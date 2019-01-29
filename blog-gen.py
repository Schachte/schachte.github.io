import datetime
import sys
import os

'''
---
  layout: post
  title: "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia"
  description: "A small river named Duden flows by their place and supplies it with the necessary regelialia."
  date: 2015-11-12 16:38:20
  comments: true
  keywords: "welcome, Far, far, away"
  category: welcome
  tags:
  - welcome
---
'''

def main():
  print('Generating file in path: ' + sys.argv[1])
  print('Blog Title: ' + sys.argv[2])
  generateFileName(sys.argv[1], sys.argv[2])

def generateFileName(filePath, blogTitle):
  now = datetime.datetime.now()
  title = blogTitle.replace(' ', '-')
  title = now.strftime("%Y-%m-%d-" + title + ".markdown")
  writeTemplate(filePath + "/" + title, blogTitle, now.strftime("%Y-%m-%d"))

def writeTemplate(fileName, title, date):
  with open(fileName, "a") as myBlogPost:
    val = ('''---
layout: post
title: "''' + title + '''"
description: ""
date:  ''' + date + ''' 00:00:00
comments: true
keywords: ""
category:
tags:
- new blog post
---
    ''')
    print(val)
    myBlogPost.write(val)
    myBlogPost.close()
    os.system("open " + fileName)

if __name__ == "__main__":
    main()