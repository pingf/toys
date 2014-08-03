'''
Created on Jul 29, 2014

@author: fcmeng
'''
import click

@click.command()
@click.option('--dir1', default='.1', help='directory') 
@click.option('--dir2', default='.2', help='directory') 
@click.argument('name1')
@click.argument('name2')
def hello(dir1,dir2,name1,name2):
    click.echo('hello--%s--%s'%(dir1,dir2))
    click.echo('%s---%s'%(name1,name2))
if __name__ == '__main__':
    hello()
