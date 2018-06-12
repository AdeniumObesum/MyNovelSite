from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from novel import models
import bson
from bson import binary
import time
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
# from bson import binary
from myNovelSite.settings import IMG_DIR
from mongoengine.queryset.visitor import Q

def get_img(req, novel_id):
    obj_id = bson.objectid.ObjectId(oid=novel_id)
    binary_content = models.NovelModel.objects(id=obj_id).all()[0].img_content
    return HttpResponse(binary_content, content_type='image/png')
    pass

# @login_required
def index(req):
    # f = open('%s5aab3ac616745.png' % IMG_DIR, 'rb')
    # data = f.read()
    # for i in range(11,20):
    #     models.NovelModel.objects.create(title="瞎编%s"%i, author="胡诌%s"%i,
    #                                      tags=["乱扯%s"%i,],
    #                                      img_content=binary.Binary(data))
    # f.close()

    return render(req, 'show_index.html')

# @login_required
def get_pager(req, query_sets):
    paginator = Paginator(query_sets, 5)
    page = req.GET.get('page')
    try:
        content_set = paginator.page(page)
    except PageNotAnInteger:
        content_set = paginator.page(1)
    except EmptyPage:
        content_set = paginator.page(paginator.num_pages)
    return content_set



def get_all(req):
    '''返回所有查询到的数据'''
    from novel.models import SEARCHORDERBY
    search_key = req.GET.get('order_by_value', '')
    order_by = req.GET.get("field",'')
    if search_key and order_by:
        query_sets = models.NovelModel.objects.filter(Q(**{order_by+"__icontains":search_key})).all()
    else:
        query_sets = models.NovelModel.objects.filter().all()
    return query_sets



# @login_required
def get_content_set(req,query_sets):
    from novel.models import NOVELMODELDISPLAY
    headers_values = []
    # print(query_sets[0]._reverse_db_field_map)
    content_set = get_pager(req, query_sets)

    field_dic = models.NovelModel._reverse_db_field_map
    for obj in content_set:
        temp_dic = {}
        for name, field_name in field_dic.items():
            if field_name in NOVELMODELDISPLAY:
                field_value = getattr(obj, field_name)
                if field_name == 'id':
                    temp_dic[field_name] = field_value
                else:
                    temp_dic[name] = field_value
        headers_values.append(temp_dic)
    return headers_values, content_set, query_sets.count()

# @login_required
def novel_list(req):
    query_sets = get_all(req)
    headers_values, content_set, all_num = get_content_set(req,query_sets)
    return render(req, 'novel/novel_list.html',
                  {"query_sets": headers_values, 'content_set': content_set, "all_num": all_num})
    pass

# @login_required
def novel_manager(req):
    from novel.models import SEARCHORDERBY
    query_sets = get_all(req)
    headers_values, content_set, all_num = get_content_set(req,query_sets)
    return render(req, 'novel/novel_manager.html',
                  {"query_sets": headers_values,
                   'content_set': content_set,
                   "all_num": all_num,
                   'search_by':SEARCHORDERBY,
                   })
    pass

# @login_required
def novel_add(req):
    '''
    title
    author
    tags
    :param req:
    :return:
    '''
    if req.method == 'POST':
        title = req.POST.get('title', '')
        author = req.POST.get('author', '')
        tags = req.POST.get('tags', '')
        tag_list = []
        if ' ' in tags:
            tag_list = tags.split(' ')
        else:
            tag_list.append(tags)

        file = req.FILES.get('img_content')
        models.NovelModel.objects.create(title=title, author=author,
                                         tags=tag_list,
                                         img_content=binary.Binary(file.read()))

    return redirect('/novel/novel_manager/')
    pass

# @login_required
def novel_edit(req, novel_id):
    obj_id = bson.objectid.ObjectId(oid=novel_id)
    obj = models.NovelModel.objects.get(id=obj_id)
    if req.method == "GET":
        return render(req, 'novel/novel_edit.html', {"obj": obj})

    if req.method == "POST":
        title = req.POST.get('title', '')
        author = req.POST.get('author', '')
        tags = req.POST.get('tags', '')
        tag_list = []
        if ' ' in tags:
            tag_list = tags.split(' ')
        else:
            tag_list.append(tags)

        file = req.FILES.get('img_content')
        if file:
            obj.update(title=title,
                       author=author,
                       tags=tag_list,
                       img_content=binary.Binary(file.read()),
                       )
        else:
            obj.update(title=title,
                       author=author,
                       tags=tag_list,
                       )

        return redirect('/novel/novel_manager/')

    pass

# @login_required
def novel_delete(req,novel_id):
    obj_id = bson.objectid.ObjectId(oid=novel_id)
    obj = models.NovelModel.objects.get(id=obj_id)
    obj.delete()
    return redirect('/novel/novel_manager/')
    pass