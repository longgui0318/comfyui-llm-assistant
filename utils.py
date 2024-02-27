from openai import OpenAI,types
import re
import os
import yaml


def is_valid_string(s):
    return s is not None and s.strip() != ""


def get_completion(prompt, response_pattern, api_url, api_key, temperature, sys_prefix, max_tokens,stop, model="local model"):
    try:
        client = OpenAI(api_key=api_key, base_url=api_url)
        messages = [{"role": "system", "content": sys_prefix},
                    {"role": "user", "content": prompt}]
        if not is_valid_string(stop):
            stop = None
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
        )
        response_str = response.choices[0].message.content
        print(f"{model} \nrequest:{prompt}\nresponse:{response_str}")
        if response_pattern:
            try:
                response_str_t = re.search(
                    response_pattern, response_str).group(0)
                if response_str_t:
                    response_str = response_str_t
            except:
                pass

        return response_str

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return prompt


config_data = None


def load_config():
    global config_data
    if config_data:
        return config_data
    my_path = os.path.dirname(__file__)
    with open(os.path.join(my_path, "config.yaml"), 'r') as file:
        # 使用yaml.load()解析YAML文件内容
        config_data = yaml.load(file, Loader=yaml.FullLoader)

    return config_data
