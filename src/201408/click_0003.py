'''
Created on Jul 29, 2014

@author: fcmeng
'''
import click


@click.group()
def cli():
    pass

@click.command()
def hello1():
    print 'hello 1'

@click.command()
@click.argument('arg1')
def hello2(arg1):
    print 'hello 2'
    print arg1

    
cli.add_command(hello1)
cli.add_command(hello2)

if __name__ == '__main__':
    cli()
