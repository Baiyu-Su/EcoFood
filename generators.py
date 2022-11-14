import os
import openai
import re

key = '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'


def text_generate(ppt, api_key, finetune):
    openai.api_key = api_key

    prompt = ppt

    print(prompt)
    # get response from GPT-3
    if finetune:
        response = openai.Completion.create(
            model="davinci:ft-oai-hackathon-2022-team-34-2022-11-14-01-27-55",
            prompt=prompt,
            temperature=0.0,
            max_tokens=1024,
            top_p=1,
            best_of=3,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        response_text = response['choices'][0]['text']
        response_list = response_text.split('\n')[1:]

        return response_list

    else:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.0,
            max_tokens=1024,
            top_p=1,
            best_of=3,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        response_text = response['choices'][0]['text']
        recipe_text = response_text.split('\n\n')
        # parse the text into three separate lists
        response_list = re.split('Name:|Ingredients:|Instructions:', response_text)[1:]
        name_list = response_list[::3]
        ingredient_list = response_list[1::3]
        instruction_list = response_list[2::3]

        # ingredient detail will be of the format:
        # [first recipe:[ingredients needed in this dish:[amount, name]], second, third]

        ingredient_detail = []
        for item in ingredient_list:
            item_list = []
            ingredients = re.split('\n', item)[:-1]
            for ingre in ingredients:
                if not re.search('-', ingre):
                    ingredients.remove(ingre)
            for ingredient in ingredients:
                splitted = ingredient.split()
                item_list.append([splitted[0] + ' ' + splitted[1], ' '.join(splitted[2:])])
            ingredient_detail.append(item_list)

        return name_list, ingredient_detail, instruction_list, recipe_text


def image_generate(recipe, api_key):
    openai.api_key = api_key
    prompt = 'Display image of food on a dish. The recipe is given as follows:' + recipe

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )

    image_url = response['data'][0]['url']

    return image_url


if __name__ == '__main__':
    prompt_1 = 'Name five low-carbon-footprint recipes that use chicken and basil'
    # prompt_1 = 'Name five low-carbon-footprint recipes that use salmon, mustard and broccoli'
    # prompt_1 = 'Name five low-carbon-footprint recipes that use beef'
    name = text_generate(prompt_1, api_key=key, finetune=True)
    print(name)

    # prompt_2 = 'How to make' + str(name[1]) + 'Display weight of each ingredient used.' \
    #            + 'Follow the format of \n Name: \n Ingredients: \n Instructions: \n'

    # name, ingredient, instruction, recipe = text_generate(prompt_2, api_key=key, finetune=False)

