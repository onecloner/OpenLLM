#!/usr/bin/env bash
# Copyright 2023 BentoML Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e

# Function to print script usage
print_usage() {
    echo "Usage: $0 [--release <major|minor|patch>]"
}

# Function to validate release argument
validate_release() {
    local release=$1

    if [[ $release == "major" || $release == "minor" || $release == "patch" ]]; then
        return 0
    else
        return 1
    fi
}

if ! [ "$GITHUB_ACTIONS" = true ]; then
    echo "This script should only be run on GitHub Actions. Aborting."
    exit 1
fi

# Check if release flag is provided
if [[ $1 == "--release" ]]; then
    # Check if release argument is provided
    if [[ -z $2 ]]; then
        echo "Error: No release argument provided."
        print_usage
        exit 1
    fi

    release=$2

    if ! validate_release "$release"; then
        echo "Error: Invalid release argument. Only 'major', 'minor', or 'patch' are allowed."
        print_usage
        exit 1
    fi
else
    echo "Error: Unknown option or no option provided."
    print_usage
    exit 1
fi

release_package() {
    local version="$1"
    echo "Releasing version ${version}..."
    jq --arg release_version "${version}" '.version = $release_version' < package.json > package.json.tmp && mv package.json.tmp package.json
    towncrier build --yes --version "${version}"
    git add CHANGELOG.md changelog.d package.json
    git commit -S -sm "infra: prepare for release ${version} [generated] [skip ci]"
    git push origin main
    echo "Releasing tag ${version}..." && git tag -a "v${version}" -sm "Release ${version} [generated by GitHub Actions]"
    git push origin "v${version}"
    echo "Finish releasing version ${version}"
}

#get highest tags across all branches, not just the current branch
version="$(git describe --tags "$(git rev-list --tags --max-count=1)")"
VERSION="${version#v}"
# Save the current value of IFS to restore it later
OLD_IFS=$IFS
IFS='.'
# split into array
read -ra VERSION_BITS <<< "$VERSION"
# Restore the original value of IFS
IFS=$OLD_IFS
VNUM1=${VERSION_BITS[0]}
VNUM2=${VERSION_BITS[1]}
VNUM3=${VERSION_BITS[2]}

if [[ $release == 'major' ]]; then
    VNUM1=$((VNUM1+1))
    VNUM2=0
    VNUM3=0
elif [[ $release == 'minor' ]]; then
    VNUM2=$((VNUM2+1))
    VNUM3=0
else
    VNUM3=$((VNUM3+1))
fi

echo "Commit count: $(git rev-list --count HEAD)"

#create new tag
RELEASE_VERSION="$VNUM1.$VNUM2.$VNUM3"
release_package "${RELEASE_VERSION}"
