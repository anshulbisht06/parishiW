from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.views.generic import TemplateView 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os, json
from pathlib import Path

data_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

@api_view(['GET'])
def demo(request):
    data = {
        'working': True
    }
    return Response(data)


class ItemsListView(TemplateView):
    template_name = "shop.html"

    def get_context_data(self, **kwargs):
        context = super(ItemsListView, self).get_context_data(**kwargs)
        context['found'] = False
        items_found = False
        category_formatted = kwargs['category'].lower().replace(' ', '_')
        data_file = Path(os.path.join(data_folder_path, '%s.json' % category_formatted ))
        if data_file.is_file():
            items_found = json.loads(open(str(data_file), 'r').read())
            if items_found:
                page = kwargs.get('page', 1)
                context['msg'] = 'Item found!'
                paginator = Paginator(items_found, 6)
                context['found'] = True
                context['category'] = kwargs['category']
                context['category_formatted'] = category_formatted
                try:
                    context['items'] = paginator.page(page)
                except PageNotAnInteger:
                    context['items'] = paginator.page(1)
                except EmptyPage:
                    context['items'] = paginator.page(paginator.num_pages)
            else:
                context['msg'] = 'No items exists under category %s' % (kwargs['category'])
        else:
                context['msg'] = 'No category exists with name %s' % (kwargs['category'])
        return context


class ItemDetailView(TemplateView):
    template_name = "single-product.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['found'] = False
        item_found = False
        data_file = Path(os.path.join(data_folder_path, '%s.json' % (kwargs['category'].lower().replace(' ', '_')) ))
        if data_file.is_file():
            items = json.loads(open(str(data_file), 'r').read())
            for item in items:
                if item['id'] == kwargs['item_id'].strip():
                    item_found = item
                    context['found'] = True
                    context['category'] = kwargs['category']
                    break
            if item_found:
                context['msg'] = 'Item found!'
                context['item'] = item_found
            else:
                context['msg'] = 'No item exists under category %s' % (kwargs['category'])
        else:
                context['msg'] = 'No category exists with name %s' % (kwargs['category'])
        return context


class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        data_files = [f for f in os.listdir(data_folder_path) if f.endswith('.json')]
        data = []
        for f in data_files:
            t = Path(os.path.join(data_folder_path, f))
            if t.is_file():
                data += json.loads(open(str(t), 'r').read())[:2]
        context['latest_items'] = data
        return context


class ErrorPageView(TemplateView):
    template_name = "error404.html"