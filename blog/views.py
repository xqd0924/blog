from django.shortcuts import render, HttpResponse, redirect
from PIL import Image, ImageDraw, ImageFont
import os
from BBS import settings
import random
from io import BytesIO
from django.contrib import auth
from django.http import JsonResponse
from blog import myforms
from blog import models

from django.db.models import Count
from django.contrib.auth.decorators import login_required
import json
# random_code=''
from django.db import transaction
from django.db.models import F


# Create your views here.
def login(request):
    if request.method == 'GET':
        dic = {'name': 'lqz', 'age': 18}
        return render(request, 'login.html', locals())
    # elif request.method=='POST':
    # 判断前台发的请求是不是ajax的请求
    elif request.is_ajax():
        response = {'user': None, 'msg': None}
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')
        # 判断传过来的验证码是否正确
        # 从session中取出来
        if valid_code.upper() == request.session.get('valid_code').upper():
            user = auth.authenticate(request, username=name, password=pwd)
            if user:
                # ajax请求,不能再返回render页面,或者redirect,只能返回字符串
                # 校验通过,一定要登录
                auth.login(request, user)
                response['user'] = name
                # response['url'] = '/index/'
                response['msg'] = '登录成功'
            else:
                # 用户名密码错误
                response['msg'] = '用户名密码错误'
        else:
            response['msg'] = '验证码错误'
    return JsonResponse(response)


from BBS import settings


def get_random_color():
    return (
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )


def get_valid_code(request):
    # 第一种方式
    # with open('static/img/lhf.jpg','rb') as f:
    #     # 图片二进制
    #     data=f.read()
    # return HttpResponse(data)
    # 第二种方式:随机生成一张图片
    # pip3 install Pillow
    # pillow 是一个图形处理的模块,功能很强强大
    # 生成一张图片,第一个参数是模式:RGB,第二个参数是图片大小,第三个参数是图片颜色
    # img = Image.new('RGB', (320, 35), color=get_random_color())
    # # 保存到本地
    # with open('valid_code.png', 'wb') as f:
    #     # 直接用img的save方法,第一个参数是空文件,第二个参数图片格式
    #     img.save(f, 'png')
    # # 打开文件,再返回
    # with open('valid_code.png', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 第三种方式
    # 在内存中生成一个空文件(把它想象成 open('valid_code.png', 'wb') as f:)
    # 一个是在硬盘上,一个是在内存中
    # img = Image.new('RGB', (320, 35), color=get_random_color())
    # f = BytesIO()
    # # 把图片保存到f中
    # # 放到内存中,存取比较快,而且有自动清理
    # img.save(f, 'png')
    #
    # data = f.getvalue()
    # return HttpResponse(data)
    # 第四种方式,在图片上写文字
    # img = Image.new('RGB', (320, 35), color=get_random_color())
    # # 拿到画笔,把图片传入画笔
    # img_draw=ImageDraw.Draw(img)
    # # 生成一个字体对象,第一个参数是字体文件的路径,第二个参数是字体大小
    # font=ImageFont.truetype('static/font/ss.TTF',size=25)
    #
    # # 第一个参数,xy的坐标,第二个参数:要写的文字,第三个参数:写文字的颜色,第四个参数:字体
    # # 不同的字体是不同的ttf文件
    # img_draw.text((0,0),'python',get_random_color(),font=font)
    #
    # f = BytesIO()
    # # 把图片保存到f中
    # # 放到内存中,存取比较快,而且有自动清理
    # img.save(f, 'png')
    #
    # data = f.getvalue()

    img = Image.new('RGB', (320, 35), color=get_random_color())
    # 拿到画笔,把图片传入画笔
    img_draw = ImageDraw.Draw(img)
    # 生成一个字体对象,第一个参数是字体文件的路径,第二个参数是字体大小
    font = ImageFont.truetype('static/font/ss.TTF', size=25)

    # 第一个参数,xy的坐标,第二个参数:要写的文字,第三个参数:写文字的颜色,第四个参数:字体
    # 不同的字体是不同的ttf文件
    random_code = ''
    # 弄一个循环,循环5次,每次随机写一个(数字,大写,小写字母)
    for i in range(5):
        char_num = random.randint(0, 9)
        # 生成一个97到122的数字,然后用chr转成字符
        char_lower = chr(random.randint(97, 122))
        char_upper = chr(random.randint(65, 90))
        char_str = str(random.choice([char_num, char_lower, char_upper]))
        img_draw.text((i * 30 + 20, 0), char_str, get_random_color(), font=font)

        random_code += char_str
    # 把验证码保存到session中
    print(random_code)
    request.session['valid_code'] = random_code
    '''
    1 生成一个随机字符串:ddddsfassda
    2 在session表中插入一条数据
    3 在cook中写入 :sessionid=ddddsfassda
    '''
    # width = 320
    # height = 35
    # for i in range(10):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     # 在图片上画线
    #     img_draw.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # for i in range(100):
    #     # 画点
    #     img_draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     # 画弧形
    #     img_draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()
    # 把图片保存到f中
    # 放到内存中,存取比较快,而且有自动清理
    img.save(f, 'png')

    data = f.getvalue()
    return HttpResponse(data)


def register(request):
    if request.method == 'GET':
        my_form = myforms.RegForm()
        return render(request, 'register.html', {'my_form': my_form})
    elif request.is_ajax():
        response = {'status': 100, 'msg': None}
        print(request.POST)
        my_form = myforms.RegForm(request.POST)
        if my_form.is_valid():
            # 存数据,返回正确信息
            # 得用create_user,回忆一下为什么
            # 定义一个字典,把清理的数据赋给它
            dic = my_form.cleaned_data
            # 移除掉确认密码字段
            dic.pop('re_password')
            # 取出上传的文件对象
            my_file = request.FILES.get('my_file')

            # 如果上传的文件为空,这个字段不传,数据库里存默认值
            if my_file:
                # 放到字典中
                dic['avatar'] = my_file
            # 存数据的时候,多肯定不行,少,可以能行(null=True),它是可以的
            user = models.UserInfo.objects.create_user(**dic)
            '''
            models.FileField 有了这个字段,存文件,以及往数据库放文件路径,统统不需要自己做了
            只需要把文件对象赋给它就可以了
            '''
            # user=models.UserInfo.objects.create_user(username=name,password=pwd,avatar=文件对象)
            # 看看存没存进去
            print(user.username)
            #     要跳转的路径
            response['url'] = '/login/'
        else:
            # 返回错误信息
            response['status'] = 101
            response['msg'] = my_form.errors
        return JsonResponse(response)


def check_username(request):
    response = {'status': 100, 'msg': None}
    name = request.POST.get('name')
    print(name)
    user = models.UserInfo.objects.filter(username=name).first()
    if user:
        response['status'] = 101
        response['msg'] = '用户名已被占用'
    return JsonResponse(response)


def index(request):
    article_list = models.Article.objects.all().order_by('-create_time')
    return render(request, 'index.html', {'article_list': article_list})


def logout(request):
    auth.logout(request)
    return redirect('/index/')


# 老的---
# def user_blog(request, username,*args,**kwargs):
#     print(username)
#     user = models.UserInfo.objects.filter(username=username).first()
#     if not user:
#         return render(request, 'error.html')
#
#
#
#     blog = user.blog
#     # 过滤这个人所有的文章(基于对象的反向,按表名小写_set.all())---article_list是queryset
#     article_list=blog.article_set.all()
#     '''
#     分类的处理
#     '''
#     # 判断category_id是否有值,如果有值,直接再过滤
#     # 先取出category_id
#     category_id = kwargs.get('category_id', None)
#     if category_id:
#         article_list=article_list.filter(category__pk=category_id)
#
#     '''
#     标签的处理
#     取出kwargs内的tag_id
#     '''
#     tag_id = kwargs.get('tag_id', None)
#     if tag_id:
#         article_list=article_list.filter(tag__pk=tag_id)
#     # 查询当前站点下所有的分类,对应的文章数
#
#     # 每个的分类,对应的文章数
#     # group by谁,就以谁做基表
#     # ret=models.Category.objects.all().annotate(coun=Count('article__title')).values('title','coun')
#     # filter在前表示where value在前表group by
#     # value在后表示取值,fileter在后,表示having
#     # 先过滤出当前站点下所有的分类
#     # ret=models.Category.objects.all().filter(blog=blog)
#     # ret=models.Category.objects.all().filter(blog=blog).values('pk').annotate(coun=Count('article__title')).values('title','coun')
#     # 结果跟上面一样
#     # ret=models.Category.objects.all().filter(blog=blog).annotate(coun=Count('article__title')).values('title','coun')
#     category_num = models.Category.objects.all().filter(blog=blog).annotate(coun=Count('article__title')).values_list(
#         'title', 'coun')
#     print(category_num)
#     # 查询当前站点下每个标签对应的文章数
#     tag_num = models.Tag.objects.all().filter(blog=blog).annotate(coun=Count('article__title')).values_list('title',
#                                                                                                             'coun')
#     print(tag_num)
#     '''
#         from django.db.models.functions import TruncMonth
#         Sales.objects
#         .annotate(month=TruncMonth('timestamp'))  # Truncate to month and add to select list
#         .values('month')  # Group By month
#         .annotate(c=Count('id'))  # Select the count of the grouping
#         .values('month', 'c')  # (might be redundant, haven't tested) select month and count
#
#     '''
#     # 查询当前站点下按年月分类的文章数
#     from django.db.models.functions import TruncMonth
#     # y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values('y_m').annotate(
#     #     coun=Count('y_m')).values('y_m', 'coun')
#     y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values('y_m').annotate(
#         coun=Count('y_m')).values_list('y_m', 'coun')
#     print(y_m_num)
#     return render(request, 'user_blog.html', locals())

# 新的
def user_blog(request, username, *args, **kwargs):
    print(username)
    # username=username
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error.html')

    blog = user.blog
    article_list = blog.article_set.all()
    # 取出condition中的分类/标签/时间
    condition = kwargs.get('condition')
    # condition可能是category|tag|archive中的一个 还可能是空
    # 取出param的值,可能为标签id,分类id,或者是时间
    param = kwargs.get('param')
    print(condition)
    print(param)
    if 'tag' == condition:
        article_list = article_list.filter(tag__pk=param)
    elif 'category' == condition:
        article_list = article_list.filter(category__pk=param)
    elif 'archive' == condition:
        #     2018-11   -->切分--->查询
        # [2018,11]
        archive_list = param.split('-')
        # 过滤:发布年为2018年,月为11月的所有文章
        article_list = article_list.filter(create_time__year=archive_list[0], create_time__month=archive_list[1])

    #
    #
    # category_num = models.Category.objects.all().filter(blog=blog).annotate(coun=Count('article__title')).values_list(
    #     'title', 'coun','pk')
    # print(category_num)
    # # 查询当前站点下每个标签对应的文章数
    # tag_num = models.Tag.objects.all().filter(blog=blog).annotate(coun=Count('article__title')).values_list('title',
    #                                                                                                         'coun','pk')
    # print(tag_num)
    # '''
    #     from django.db.models.functions import TruncMonth
    #     Sales.objects
    #     .annotate(month=TruncMonth('timestamp'))  # Truncate to month and add to select list
    #     .values('month')  # Group By month
    #     .annotate(c=Count('id'))  # Select the count of the grouping
    #     .values('month', 'c')  # (might be redundant, haven't tested) select month and count
    #
    # '''
    # # 查询当前站点下按年月分类的文章数
    # from django.db.models.functions import TruncMonth
    # # y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values('y_m').annotate(
    # #     coun=Count('y_m')).values('y_m', 'coun')
    # y_m_num = models.Article.objects.all().filter(blog=blog).annotate(y_m=TruncMonth('create_time')).values(
    #     'y_m').annotate(
    #     coun=Count('y_m')).values_list('y_m', 'coun')
    # print(y_m_num)
    return render(request, 'user_blog.html', locals())


def article_detail(request, username, id):
    print(username)
    username = username
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, 'error.html')

    blog = user.blog

    article = models.Article.objects.filter(pk=id).first()
    #   取出文章所有评论,从文章,查询评论
    # 基于对象的反向查询
    # content_list=models.Commit.objects.filter(article=article)

    content_list = article.commit_set.all().order_by('pk')

    return render(request, 'article_detail.html', locals())


# @login_required(login_url='/login/')
# @login_required
# def diggit(request):
#     response={'status':100,'msg':None}
#
#
#     if request.user.is_authenticated():
#         # 从前端传过来的数据,都转成str类型
#         article_id=request.POST.get('article_id')
#         is_up=request.POST.get('is_up')
#         print(is_up)
#         print(type(is_up))
#         # 用json转
#         # # python中的
#         # {'is_up':True}
#         # # 转成json
#         # {"is_up": "true"}
#         is_up=json.loads(is_up)
#         print(is_up)
#         print(type(is_up))
#         # 原子性操作.用事务
#         with transaction.atomic():
#             models.UpAndDown.objects.create(user=request.user,article_id=article_id,is_up=is_up)
#             models.Article.objects.filter(pk=article_id).update(up_num=F('up_num')+1)
#             response['msg']='点赞成功'
#     else:
#         response['msg'] = '请先登录'
#         response['status'] = 101
#     return JsonResponse(response)


def diggit(request):
    response = {'status': 100, 'msg': None}

    if request.user.is_authenticated():
        # 从前端传过来的数据,都转成str类型
        article_id = request.POST.get('article_id')
        is_up = request.POST.get('is_up')
        is_up = json.loads(is_up)
        user = request.user
        # 存之前先查询,当前用户对该篇文章是否点过
        ret = models.UpAndDown.objects.filter(user_id=user.pk, article_id=article_id).exists()
        if ret:
            # 当有数据,说明,已经点过赞或者踩了
            response['msg'] = '您已经点过了'
            response['status'] = 101
        else:
            # 原子性操作.用事务
            with transaction.atomic():
                models.UpAndDown.objects.create(user=user, article_id=article_id, is_up=is_up)
                # 先取出文章的queryset对象
                article = models.Article.objects.filter(pk=article_id)
                if is_up:
                    article.update(up_num=F('up_num') + 1)
                    response['msg'] = '点赞成功'
                else:
                    article.update(down_num=F('down_num') + 1)
                    response['msg'] = '反对成功'
    else:
        response['msg'] = '请先登录'
        response['status'] = 102
    return JsonResponse(response)


from django.core.mail import send_mail


def commit_content(request):
    response = {'status': 100, 'msg': None}
    if request.is_ajax():
        if request.user.is_authenticated():
            # 核心逻辑
            user = request.user
            article_id = request.POST.get('article_id')
            content = request.POST.get('content')
            pid = request.POST.get('pid')
            with transaction.atomic():
                ret = models.Commit.objects.create(user=user, article_id=article_id, content=content, parent_id=pid)
                models.Article.objects.filter(pk=article_id).update(commit_num=F('commit_num') + 1)

            response['msg'] = '评论成功'
            response['content'] = ret.content
            # 把datetime类型转成字符串,因为json是无法序列化datetime
            response['time'] = ret.create_time.strftime('%Y-%m-%d %X')
            response['user_name'] = ret.user.username
            if pid:
                # 如果是字评论,返回父评论的名字
                response['parent_name'] = ret.parent.user.username
            #     评论成功,发送邮件
            '''
            subject:邮件标题
            message:邮件内容
            from_email:邮件发送者
            recipient_list:接收者列表,可以传多个
            '''
            from BBS import settings
            # 会有返回值,邮件发送成功是true
            # 拿到文章标题
            atricle_name = ret.article.title
            # 被当前登录人评论
            usre_name = request.user.username
            # 这个是一个同步的操作:等邮件发完,才能继续往下走(耗时的操作,应该怎么做?可以开一个线程)
            # ret=send_mail('您的%s文章被%s评论了'%(atricle_name,usre_name),'这个人评论了:%s'%(content,),settings.EMAIL_HOST_USER,['616564099@qq.com'] )
            from threading import Thread
            # 实例化
            t1 = Thread(target=send_mail, args=(
                '您的%s文章被%s评论了' % (atricle_name, usre_name), '这个人评论了:%s' % (content,), settings.EMAIL_HOST_USER,
                ['616564099@qq.com']))
            t1.start()

        else:
            response['status'] = 101
            response['msg'] = '您没有登录'
    else:
        response['status'] = 101
        response['msg'] = '您请求非法'
    return JsonResponse(response)


@login_required(login_url='/login/')
def backend(request):
    if request.method == 'GET':
        # 查询出当前登录用户的所有文章
        blog = request.user.blog
        article_list = models.Article.objects.filter(blog=blog)
        return render(request, 'back/backend.html', {"article_list": article_list})


from bs4 import BeautifulSoup


@login_required(login_url='/login/')
def add_article(request):
    '''
    用一个模块:BeautifulSoup4---bs4---做爬虫,解析html页面
    -安装
    -使用  导入 from bs4 import BeautifulSoup
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'back/add_article.html', )

    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 第一个参数:要解析的html内容,第二个参数:以什么解析器,解析我的页面
        # html.parser 是bs4 内置的解析器.也可以lxml,但是需要安装
        soup = BeautifulSoup(content, 'html.parser')
        # soup=BeautifulSoup(content,'lxml')

        # 通过bs4模块,去掉script标签,处理xss攻击
        # 查询出所有的标签
        tags = soup.find_all()
        # tags=soup.find_all('span',attrs={'class':'errors'})
        for tag in tags:
            # print(tag)
            if tag.name == 'script':
                # 过滤出是sctipt的标签
                # 删除掉script的标签
                tag.decompose()
            print('-----------------------------')
        print(soup)
        # 取出html标签中所有文本内容
        # print(soup.text)
        # 截取文字的前150个,作为摘要
        desc = soup.text[0:150]
        ret = models.Article.objects.create(title=title, desc=desc, content=str(soup), blog=request.user.blog)
        return redirect('/backend/')


# 可以局部禁用csrf
def upload_img(request):
    # 传上来的图片,是文件
    # 是文件,从哪取?
    print(request.FILES)
    myfile = request.FILES.get('myfile')

    path = os.path.join(settings.BASE_DIR, 'media', 'img')
    # 不存在这个文件夹
    if not os.path.isdir(path):
        os.mkdir(path)
    file_path = os.path.join(path, myfile.name)
    with open(file_path, 'wb') as f:
        for line in myfile:
            f.write(line)

    # 按照要求来处理
    '''
            //成功时
        {
                "error" : 0,
                "url" : "http://www.example.com/path/to/file.ext"
        }
        //失败时
        {
                "error" : 1,
                "message" : "错误信息"
        }
    '''
    dic = {'error': 0, 'url': '/media/img/%s' % myfile.name}
    return JsonResponse(dic)


@login_required
def update_head(request):
    if request.method=='GET':
        return render(request,'update_head.html')
    else:
        myfile = request.FILES.get('head')
        # 可以只删除数据库的地址,不删实际文件
        user = request.user
        user.avatar = myfile
        user.save()

        # 如果直接这样更新,不会带avatar那个路径,所以不能用这种方式来更新
        # ret=models.UserInfo.objects.filter(pk=request.user.pk).update(avatar=myfile)

        return redirect('/index/')


# def update_article(request,pk):
#     if request.method=='GET':
#         article=models.Article.objects.get(pk=pk)
#         return render(request,'back/update_article.html',{'article':article})


def update_article(request,pk):
    if request.method=='GET':
        return render(request,'back/update_article2.html',{'article_id':pk})


def get_article(request,pk):
    article=models.Article.objects.get(pk=pk)

    return JsonResponse({'title':article.title,'content':article.content})


