# encoding: utf-8
# author = 'Albert_Musk'

from redis import Redis

cache = Redis(host='127.0.0.1',port=6379)

def set(key,value,ex=120):
    return cache.set(key,value,ex)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)

if __name__ == '__main__':
    cache.set('username','helloworld')
    if cache.get('username').decode() == 'helloworld':
        print('True')
    else:
        print('False')