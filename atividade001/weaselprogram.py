import string
import random
import time
start_time = time.time()

#Start of the program
print(
    "Olá! O seguinte programa tentará fazer uma 'mutação' a partir de "
    "uma string aleatória para chegar na frase "
    "'METHINKS IT IS LIKE A WEASEL'\n"
)

#Declaring the charactes
POSSIBLE_CHARS_LETTERS = string.ascii_uppercase + " "
POSSIBLE_CHARS_NUMERALS = "0123456789"

#While Structure for user input
while True:

    #Asking the user answer for generating a random string
    inicial_answer = input(
        'Deseja digitar uma string para o programa fazer a "mutação" dela? '
        "(s/n) "
    )

    #Positive answer
    if inicial_answer.lower() in ("s", "sim"):
        while True:
            print(
                "Para que ele funcione adequadamente, você deverá digitar "
                "uma string de acordo com as regras à seguir:\n"
            )
            print("A string deve ter 28 caracteres\n")

            initial_phrase = input(
                "Digite a string inicial de 28 caracteres para "
                "iniciarmos o processo: "
            )
            print(f'Você digitou a string: "{initial_phrase}"\n')

            string_size = len(initial_phrase)

            if not initial_phrase.isupper():
                if not initial_phrase.isdigit():
                    print("Não há apenas letras maiúsculas na string")

            if string_size != 28:
                print("Não há 28 caracteres na string")

            if (initial_phrase.isupper() and string_size == 28) or (
                initial_phrase.isdigit()
            ):
                break
        break

    #Negative answer
    elif inicial_answer.lower() in ("n", "não", "nao"):
        print("\nTudo bem! Geraremos uma string aleatória.\n")

        letters_or_numbers = input("1) para letras\n2) para números: ")

        if letters_or_numbers in ("1", "1)"):
            initial_phrase = "".join(
                random.choices(POSSIBLE_CHARS_LETTERS, k=28)
            )
        elif letters_or_numbers in ("2", "2)"):
            initial_phrase = "".join(
                random.choices(POSSIBLE_CHARS_NUMERALS, k=28)
            )

        print(f'A string gerada foi: "{initial_phrase}"\n')
        break

    else:
        print("Não entendi sua resposta, pode responder novamente?")

    break


# Defines objetive depending from user choice
if letters_or_numbers in ("1", "1)"):
    objective_phrase = "METHINKS IT IS LIKE A WEASEL"
elif letters_or_numbers in ("2", "2)"):
    objective_phrase = "1231231231231231231231231231"

#Declaring main variables for mutation
print("O processo de mutação iniciará agora...\n")
current_main_phrase = initial_phrase
mutation_rate = 5

best_phrase = current_main_phrase
best_correct = 0
generation_counter = 1
max_generations = 100

#Entering 
while (
    current_main_phrase != objective_phrase
    and generation_counter <= max_generations
):
    dinamic_list = []
    interior_correct_char_counter = 0

    #Looking into string comparison
    for i, char in enumerate(current_main_phrase):
        if char == objective_phrase[i]:
            dinamic_list.append(char)
            interior_correct_char_counter += 1
        else:
            dinamic_list.append("-")

    # Saving data from mutation
    while True:
        next_chars = []
        for i, char in enumerate(dinamic_list):
            if char == objective_phrase[i]:
                next_chars.append(char)
            else:
                #Based on user input
                if random.randint(0, 101) <= mutation_rate:
                    if letters_or_numbers in ("1", "1)"):
                        next_chars.append(random.choice(POSSIBLE_CHARS_LETTERS))
                    if letters_or_numbers in ("2", "2)"):
                        next_chars.append(
                            random.choice(POSSIBLE_CHARS_NUMERALS)
                        )
                else:
                    next_chars.append(current_main_phrase[i])

        mutated_phrase = "".join(next_chars)

        #Counting correct answers
        new_correct = 0
        for i, c in enumerate(mutated_phrase):
            if c == objective_phrase[i]:
                new_correct += 1

        # Deciding which is the best string
        if new_correct > interior_correct_char_counter:
            current_main_phrase = mutated_phrase
            interior_correct_char_counter = new_correct
            break

    if interior_correct_char_counter > best_correct:
        best_correct = interior_correct_char_counter
        best_phrase = current_main_phrase

    #Showing the results as it loads
    print(f"Geração: {generation_counter}")
    print(f"Antes da mutação: {''.join(dinamic_list)}")
    print(f"Após a mutação: {current_main_phrase}")
    print(
        f"Caracteres corretos na geração após mutação: "
        f"{interior_correct_char_counter}\n"
    )

    generation_counter += 1

#Registering the time
end_time = time.time()
execution_time = end_time - start_time
print(f"Tempo de execução: {execution_time:.2f} segundos")