#!/usr/bin/env python

from navigator import Navigator


n = Navigator()
n.setAuth('basic','user','pass')
n.go('https://127.0.0.1','lalala')


