import subprocess
import string

def check(command, text, word_mode=False):
    try:
        output = subprocess.check_output(command, shell=True, text=True)

        if word_mode:
            # Разбиваем текст на слова, удаляем знаки пунктуации
            words = [''.join(c for c in word if c not in string.punctuation) for word in output.split()]
            return text in words
        else:
            return text in output
    except subprocess.CalledProcessError:
        return False

if __name__ == '__main__':
    command = "cat /home/ub/test.ssh"
    text = 'The test'

    if check(command, text):
        print('SUCCESS')
    else:
        print('FAIL')

    word_to_find = 'test'

    if check(command, word_to_find, word_mode=True):
        print('Word found')
    else:
        print('Word not found')
