#!/usr/bin/python3
"""Comand Interpreter
"""
import re
import cmd
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command Interpreter Class.
    """

    prompt = '(hbnb) '
    classes = {'BaseModel', 'User', 'State', 'City', 'Amenity',
               'Place', 'Review'}

    def do_quit(self, person):
        """Command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """Handles the Ends Of File signal with a newline.
        """
        print()
        return True

    def emptyline(self):
        """Handles Empty Line Command.
        """
        pass

    def do_create(self, args):
        """Create a new instance of a class.

        Args:
            arg (str): The name of the class to create an instance of.
            arg <class name>.count(): Retrieves the number of instances.
        """
        if not args:
            print("** class name missing **")
        else:
            arg = args.split()

            if arg[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                if len(arg) < 2:
                    obj = eval(arg[0])()
                else:
                    kwargs = {}

                    for i in range(1, len(arg)):
                        key, value = tuple(arg[i].split('='))

                        pattern = r'^"(.*?)"$'
                        match = re.match(pattern, value)

                        if match:
                            value = value.strip('"').replace('_', ' ')
                        else:
                            value = eval(value)
                        kwargs[key] = value

                    obj = eval(arg[0])(**kwargs)

                obj.save()
                print(obj.id)

    def do_show(self, args):
        """Show details of a specific instance.

        Args:
            args (str): The class name and instance id separated by space.
            arg <class name>.show("<id>"): Retrieves an instance based on its ID
        """
        if not args:
            print("** class name missing **")
        else:
            arg = args.split()

            if arg[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(arg) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg[0], arg[1])

                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, args):
        """Delete an instance from storage.

        Args:
            args (str): The class name and instance id separated by space.
            arg <class name>.destroy("<id>"): Destroys an instance by ID.
        """
        if not args:
            print("** class name missing **")
        else:
            arg = args.split()

            if arg[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(arg) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg[0], arg[1])

                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, args):
        """Print all string representation of all instances.

        Args:
            arg (str): The class name (optional).
            arg <class name>.all(): Retrieves all instances of a class.
        """
        if not args:
            print([str(obj) for obj in storage.all().values()])
        else:
            arg = args.split()
            if arg[0] not in self.classes:
                print("** class doesn't exist **")
            else:
                print([str(obj) for obj in storage.all().values()
                       if arg[0] == type(obj).__name__])

    def do_update(self, args):
        """Updates an attribute of an instance of a class.

        Args:
            args (str): A string containing the class name, instance ID,
            attribute name, and value to be updated.
            arg <class name>.update("<id>", <attribute name>, <attribute value>):
            Update an instance based on his ID.
            arg <class name>.update("<id>", <dictionary representation>):
            update an instance based on his ID with a dictionary.
        """
        if not args:
            print("** class name missing **")
        else:
            arg = args.split()

            if arg[0] not in self.classes:
                print("** class doesn't exist **")
            elif len(arg) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(arg[0], arg[1])

                if key not in storage.all():
                    print("** no instance found **")
                elif len(arg) < 3:
                    print("** attribute name missing **")
                elif len(arg) < 4:
                    print("** value missing **")
                else:
                    obj = storage.all()[key]
                    setattr(obj, arg[2], eval(arg[3]))
                    obj.save()

    def default(self, args):
        """Handles other commands that are not documented"""
        pattern = r'^(\w+)\.(\w+)(?:\(([^)]*)\))$'
        command_string = args
        match = re.search(pattern, command_string)
        if not match:
            print("*** Unknown syntax:", args)
            return
        obj_name = match.group(1)
        method = match.group(2)
        obj_args = match.group(3)
        args_pattern = r'^"([^"]*)"(?:, (.*))?$'
        args_match = re.search(args_pattern, obj_args)
        if args_match:
            obj_id = args_match.group(1)
            attr = args_match.group(2)

        if obj_name not in self.classes:
            print("** class doesn't exist **")
        else:
            if not obj_args:
                if method == 'all':
                    return self.do_all(obj_name)
                elif method == 'count':
                    print(len([obj for obj in storage.all().values()
                               if obj_name == type(obj).__name__]))
                else:
                    print("*** Unknown syntax:", args)
            else:
                if not args_match:
                    obj_id = obj_args
                    print("*** Unknown syntax:", args)
                    return

                if not attr:
                    if method == 'show':
                        show = "{} {}".format(obj_name, obj_id)
                        self.do_show(show)
                    elif method == 'destroy':
                        destroy = "{} {}".format(obj_name, obj_id)
                        self.do_destroy(destroy)
                    else:
                        print("*** Unknown syntax:", args)
                else:
                    if method == 'update':
                        dict_pattern = (r'^({["\'][^\"]+["\']\s*:\s*(["\']'
                                        r'[^"\']+["\']|\d+(\.\d+)?)(?:,\s*'
                                        r'["\'][^\"]+["\']\s*:\s*(["\'][^"\']+'
                                        r'["\']|\d+(\.\d+)?))*})$')
                        dict_match = re.search(dict_pattern, attr)

                        key_value_pattern = (r'^["\'](.*)["\'](?:, (["\'].*'
                                             r'["\']$|\d+(\.\d+)?))')
                        key_value_match = re.search(key_value_pattern, attr)
                        if dict_match:
                            dictionary = dict_match.group(1)
                            for key, value in eval(dictionary).items():
                                if type(value) is str:
                                    update = '{} {} {} "{}"'.format(
                                        obj_name, obj_id, key, value)
                                else:
                                    update = '{} {} {} {}'.format(
                                        obj_name, obj_id, key, value)
                                self.do_update(update)
                        elif key_value_match:
                            obj_key = key_value_match.group(1)
                            obj_value = key_value_match.group(2)
                            update = '{} {} {} {}'.format(
                                obj_name, obj_id, obj_key, obj_value)
                            self.do_update(update)
                        else:
                            print("*** Unknown syntax:", args)


if __name__ == '__main__':
    HBNBCommand().cmdloop()