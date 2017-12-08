'''
A module to handle menus.
'''
class Menu():
    def __init__(self,title,options):
        '''The options should be a list'''
        self.__title = title
        self.__options = options
        self.__main_title = None

    def set_main_title(self, main_title):
        '''
        If you want to change the main tilte
        '''
        self.__main_title = main_title

    def display_main_menu(self):
        '''
        Prints the main title for the menu
        '''
        ascii_art='''
___  ___      _        ___  ___                 
|  \/  |     (_)       |  \/  |                 
| .  . | __ _ _ _ __   | .  . | ___ _ __  _   _ 
| |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |
| |  | | (_| | | | | | | |  | |  __/ | | | |_| |
\_|  |_/\__,_|_|_| |_| \_|  |_/\___|_| |_|\__,_|'''
        main_title = ascii_art if self.__main_title is None else self.__main_title
        print(main_title)
        return self.get_single_choice()

    def banner(self):
        '''
        Prints the menu banner
        '''
        if self.__title is None:
            return
        print('--------------------')
        print(self.__title.center(20))
        print('--------------------')

    def display_options(self, options):
        '''
        Displays choices for user
        '''
        count = 1
        valid_options = list()
        for option in options:
            valid_options.append(count)
            print(str(count)+'.'+str(option))
            count += 1
        return valid_options

    def get_single_choice(self):
        '''
        Gets a single choice from user
        '''
        input_message = '\n>>>Enter Your Choice : '
        invalid_option_message = '\n>>>Please, Enter a Valid Option : '

        self.banner()
        options = self.__options

        valid_options = self.display_options(options)
        choice = input(input_message)

        if choice.isdigit() and int(choice) in valid_options:
            choice_int = int(choice)
            return options[choice_int-1]
        else:
            print(invalid_option_message)
            return self.get_single_choice()



    def get_multiple_options(self, exit_function):
        '''
        Gets multiple options from user
        '''
        self.banner()
        options = self.__options
        valid_options = self.display_options(options)

        input_message = ">>>Enter options seperated by comma or 'skip': "
        invalid_option_message = ">>>Enter correct options. Try again."
        choices = input(input_message)

        if choices.lower() == 'exit' or choices.lower() == 'skip':
            return exit_function()

        choices = choices.strip().split(',')
        choice_list = list()

        for choice in choices:
            if choice.isdigit() and int(choice) in valid_options:
                choice_list.append(int(choice))
            else:
                break

        if len(choices) != len(choice_list):
            print(invalid_option_message)
            return self.get_multiple_options(exit_function)

        chosen_options = list()
        for i in list(set(choice_list)):
            chosen_options.append(options[i-1])

        return chosen_options