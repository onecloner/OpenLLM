from __future__ import annotations
import argparse
import asyncio
import json

import aiohttp

import openllm

async def send_request(url, prompt, session, model, **attrs):
  headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
  config = openllm.AutoConfig.for_model(model).model_construct_env(**attrs).model_dump()
  data = {'prompt': prompt, 'llm_config': config, 'adapter_name': None}
  async with session.post(url, headers=headers, data=json.dumps(data)) as response:
    result = await response.text()
  print('-' * 10 + '\n\n prompt:', prompt, '\nGeneration:', result, '\n\n' + '-' * 10)

async def main(args: argparse.Namespace) -> int:
  endpoint = 'generate' if args.generate else 'generate_stream'
  url = f'http://localhost:3000/v1/{endpoint}'
  # len=100
  prompts = [
      'What is the meaning of life?',
      'Explain the concept of quantum entanglement.',
      'Describe the process of photosynthesis.',
      'What are the benefits of regular exercise?',
      'How does the internet work?',
      'Discuss the impact of climate change on ecosystems.',
      'Explain the principles of supply and demand in economics.',
      'What is the history of the Roman Empire?',
      'Describe the structure of a cell.',
      'Discuss the pros and cons of renewable energy sources.',
      'Explain the theory of relativity.',
      'What is the role of DNA in genetics?',
      'Describe the art movement of the Renaissance.',
      'Discuss the causes of World War I.',
      'What are the major functions of the human brain?',
      'Explain the process of evolution by natural selection.',
      'Describe the cultural significance of the Great Wall of China.',
      'What is the impact of social media on society?',
      'Discuss the life and works of Shakespeare.',
      'Explain the concept of artificial intelligence.',
      'What are the different types of chemical reactions?',
      "Describe the structure of the Earth's atmosphere.",
      'Discuss the history of the civil rights movement.',
      'What are the economic implications of globalization?',
      'Explain the principles of good nutrition.',
      'Describe the major functions of the immune system.',
      'Discuss the impact of colonialism on Africa.',
      'What is the process of cellular respiration?',
      'Explain the importance of biodiversity.',
      'Discuss the causes and consequences of the Industrial Revolution.',
      'What are the fundamental principles of democracy?',
      'Describe the major components of a computer.',
      'Explain the concept of human rights.',
      'What is the role of enzymes in biological reactions?',
      'Discuss the history of space exploration.',
      'What are the ethical considerations in medical research?',
      'Describe the cultural significance of the Pyramids of Egypt.',
      'Explain the principles of classical physics.',
      'What is the impact of climate change on weather patterns?',
      'Discuss the major events of the American Revolution.',
      'What are the effects of pollution on the environment?',
      'Describe the process of protein synthesis.',
      'Explain the concept of sustainable agriculture.',
      'What is the history of the European Union?',
      'Discuss the impact of the Renaissance on art and culture.',
      'What are the key principles of marketing?',
      'Explain the structure of the periodic table.',
      'Describe the major types of renewable energy.',
      'Discuss the causes and consequences of the French Revolution.',
      'What is the role of the United Nations in international relations?',
      'Explain the principles of game theory in economics.',
      'What are the stages of human development?',
      'Describe the cultural significance of the Taj Mahal.',
      'Discuss the major themes in the works of Ernest Hemingway.',
      'What is the impact of automation on the workforce?',
      'Explain the concept of genetic engineering.',
      'What are the different types of chemical bonds?',
      "Describe the layers of the Earth's atmosphere.",
      "Discuss the history of the women's suffrage movement.",
      'What are the economic factors influencing consumer behavior?',
      'Explain the principles of conflict resolution.',
      'What is the role of neurotransmitters in the nervous system?',
      'Discuss the impact of colonialism on India.',
      'What is the process of mitosis?',
      'Explain the importance of water conservation.',
      'Describe the cultural significance of the Acropolis in Athens.',
      'Discuss the major philosophical ideas of Plato.',
      'What are the principles of investment in finance?',
      'Explain the structure of a virus.',
      'What is the history of the United Nations?',
      'Discuss the impact of technology on modern art.',
      'What are the key concepts in cognitive psychology?',
      'Describe the major types of non-renewable energy sources.',
      'Explain the causes and consequences of the Russian Revolution.',
      'What is the role of the World Health Organization in global health?',
      'Discuss the principles of ethics in business.',
      'What are the stages of the water cycle?',
      'Explain the concept of social justice.',
      'What is the impact of deforestation on climate change?',
      'Describe the process of meiosis.',
      'Discuss the cultural significance of the Sistine Chapel ceiling.',
      'What are the major themes in the novels of Jane Austen?',
      'Explain the role of branding in marketing.',
      'What is the history of the Internet?',
      'Discuss the impact of artificial intelligence on society.',
      'What are the principles of statistical analysis in research?',
      'Explain the structure of an atom.',
      'What is the significance of the Theory of Evolution by Charles Darwin?',
      'Describe the major types of renewable energy.',
      'Discuss the causes and consequences of the American Civil War.',
      'What is the role of the International Monetary Fund in global economics?',
      'Explain the principles of environmental conservation.',
      'What are the stages of the rock cycle?',
      'Describe the concept of cultural relativism.',
      'Discuss the major contributions of Leonardo da Vinci to art and science.',
      'What is the impact of globalization on cultural diversity?',
      'Explain the process of genetic inheritance.',
      'What are the different forms of government in the world?',
      'Describe the major types of pollution.',
      'Discuss the history of the labor movement.',
      'What are the principles of sustainable urban planning?',
      'Explain the role of hormones in the endocrine system.',
      'What is the cultural significance of the Great Barrier Reef?',
      'Discuss the major ideas of Friedrich Nietzsche.',
      'What is the impact of social media on political movements?',
      'Explain the concept of quantum computing.',
      'What are the principles of international diplomacy?',
      'Describe the major types of ocean ecosystems.',
      'Discuss the causes and consequences of the Cold War.',
      'What is the role of the World Trade Organization in global trade?',
      'Explain the principles of behavioral psychology.',
      'What are the stages of the nitrogen cycle?',
      'Describe the concept of cultural appropriation.',
      'Discuss the major works of Vincent van Gogh.',
  ]
  async with aiohttp.ClientSession() as session:
    await asyncio.gather(*[send_request(url, prompt, session, 'llama', max_new_tokens=4096, top_p=0.21) for _, prompt in enumerate(prompts)])
  return 0

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--generate', default=False, action='store_true', help='Whether to test with stream endpoint.')
  args = parser.parse_args()
  raise SystemExit(asyncio.run(main(args)))