# coding=utf8

def main():
    sql = 'insert into pics_info (url,title,tags,limg_path,date) values (%s,%s)'
    li = ['abc','efg']
    print(sql % tuple(li))

if __name__ == '__main__':
    main()

