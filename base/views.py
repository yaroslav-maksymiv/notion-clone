import json

from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status, filters, viewsets
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404

from .models import (
    Page, Page_element, Text, Heading_1, Heading_2,
    PageLink, To_do, Code
)
from .serializers import (
    PageSerializer, PageFullSerializer, PageChildrenSerializer,
    Page_elementSerializer, TextSerializer, To_doSerializer,
    CodeSerializer
)


class PageElementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update')
    def update_element(self, request, pk=None):
        """ Update page element """

        order = request.POST.get('order')
        color = request.POST.get('color')

        element = get_object_or_404(Page_element, pk=pk)
        element.order_on_page = float(order)
        element.save()

        return Response(Page_elementSerializer(element).data)

    @action(detail=True, methods=['delete'], url_path='delete')
    def delete_element(self, request, pk=None):
        """ Delete page element """

        page_element = get_object_or_404(Page_element, pk=pk)
        page_element.delete()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='last-element-id')
    def get_last_element_id(self, request):
        """
        Returns last page element id
        """
        last_element_id = Page_element.objects.order_by('-id').first().id
        return Response(last_element_id)

    @action(detail=False, methods=['post'], url_path='create')
    def create_page_element(self, request):
        """
        Create element on the page
        """
        data = request.data
        element_type = data.get('type')
        order_on_page = data.get('order')
        page_id = data.get('pageId')
        element = json.loads(data.get('element', {}))

        page_instance = get_object_or_404(Page, pk=int(page_id))
        new_page_element = Page_element.objects.create(
            page=page_instance,
            element_type=element_type,
            order_on_page=float(order_on_page)
        )

        if element_type == 'Text':
            Text.objects.create(
                text=element.get('text', ''),
                page_element=new_page_element
            )
        elif element_type == 'Heading 1':
            Heading_1.objects.create(
                heading_text=element.get('heading', ''),
                page_element=new_page_element
            )
        elif element_type == 'Heading 2':
            Heading_2.objects.create(
                heading_text=element.get('heading', ''),
                page_element=new_page_element
            )
        elif element_type == 'To-do':
            To_do.objects.create(
                page_element=new_page_element
            )
        elif element_type == 'Code':
            Code.objects.create(
                code=element.get('code', ''),
                language=element.get('language', ''),
                page_element=new_page_element
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(Page_elementSerializer(new_page_element).data)

    @action(detail=True, methods=['post'], url_path='update-element')
    def update_page_element(self, request, pk=None):
        """
        Update elements
        """
        element_type = request.data.get('type')
        data = json.loads(request.data.get('data'))

        if element_type == 'Text':
            element_instance = get_object_or_404(Text, pk=pk)
            element_instance.text = data.get('text')
        elif element_type == 'Heading 1':
            element_instance = get_object_or_404(Heading_1, pk=pk)
            element_instance.heading_text = data.get('heading')
        elif element_type == 'Heading 2':
            element_instance = get_object_or_404(Heading_2, pk=pk)
            element_instance.heading_text = data.get('heading')
        elif element_type == 'To-do':
            element_instance = get_object_or_404(To_do, pk=pk)
            element_instance.completed = data.get('completed')
            element_instance.description = data.get('description')
        elif element_type == 'Code':
            print(data.get('code'), data.get('language'))
            element_instance = get_object_or_404(Code, pk=pk)
            element_instance.code = data.get('code')
            element_instance.language = data.get('language')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        page_element_instance = element_instance.page_element
        page_instance = page_element_instance.page
        page_creator = page_instance.creator.first()

        if page_creator == request.user:
            element_instance.save()
            return Response(Page_elementSerializer(page_element_instance).data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        

class PageSearchView(ListAPIView):
    """
    Search by name and text inside page
    Also have ordering by create and edit dates 
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'edited_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(creator=self.request.user)
        search_query = self.request.query_params.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        return queryset


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_first_page_id(request):
    exclude_page = request.POST.get('exclude_page')

    pages = Page.objects.filter(parent=None)
    if exclude_page:
        pages.exclude(pk=int(exclude_page))

    first_page = pages.order_by('id').first()
    if first_page:
        return Response({'id': first_page.id})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_page_children(request, pk):
    """
    Get all children of the current page
    """
    page = get_object_or_404(Page, pk=pk, creator=request.user)
    return Response(PageChildrenSerializer(page).data)


class PageDeleteView(DestroyAPIView):
    """
    Delete page and page link element if the one exists
    """
    queryset = Page.objects.all()

    def get_object(self):
        obj = get_object_or_404(
            Page, pk=self.kwargs['pk'], creator=self.request.user
        )
        try:
            page_link = PageLink.objects.get(page=obj)
            page_element = page_link.page_element
            page_link.delete()
            page_element.delete()
        except:
            pass
        return obj


class PageListView(ListAPIView):
    """
    Get list of pages
    """
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(creator=self.request.user, parent=None)


class PageFavouriteListView(ListAPIView):
    """
    Get list of favourite pages
    """
    serializer_class = PageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(creator=self.request.user, favourite=True)


def update_page(request, pk, update_func):
    page = get_object_or_404(Page, pk=pk, creator=request.user)
    update_func(page)
    page.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_page_to_favourite(request, pk):
    page = get_object_or_404(Page, pk=pk, creator=request.user)
    page.favourite = not page.favourite
    page.save()
    result = PageSerializer(page).data
    return Response(result)
    # def update_func(page):
    #     page.favourite = not page.favourite

    # return update_page(request, pk, update_func)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_page_title(request, pk):
    def update_func(page):
        page.name = request.POST.get('newTitle')

    return update_page(request, pk, update_func)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_page_icon(request, pk):
    def update_func(page):
        page.photo = request.POST.get('newIcon')

    return update_page(request, pk, update_func)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_page_locked(request, pk):
    def update_func(page):
        page.locked = json.loads(request.POST.get('locked'))
        print(page.locked)

    return update_page(request, pk, update_func)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_page_full_width(request, pk):
    def update_func(page):
        page.full_width = json.loads(request.POST.get('fullWidth'))

    return update_page(request, pk, update_func)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_page(request):
    """
    Create new page and add base text element
    If page has parent, then also create link page element on parent page
    """
    parent_id = request.POST.get('parent')
    parent_page = None

    # check if has parent page
    if parent_id:
        parent_page = get_object_or_404(Page, pk=int(parent_id))

        # create link page element
        max_order_on_page = parent_page.page_elements.aggregate(Max('order_on_page'))[
            'order_on_page__max']
        next_order = max_order_on_page + 1 if max_order_on_page else 1

        parent_page_element = Page_element.objects.create(
            page=parent_page,
            element_type='Page',
            order_on_page=next_order
        )

    new_page = Page.objects.create()
    new_page.parent = parent_page
    new_page.creator.add(request.user)
    new_page.save()

    # create page link with newly created page on the parent page
    if parent_page:
        link_element = PageLink.objects.create(
            page=new_page,
            page_element=parent_page_element
        )

    # add base element to the new page
    page_element = Page_element.objects.create(
        page=new_page,
        element_type='Text',
        order_on_page=1,
    )
    text = Text.objects.create(
        text='',
        page_element=page_element
    )

    page = PageSerializer(new_page).data
    return Response(page, status=status.HTTP_200_OK)


class PageSingleView(RetrieveAPIView):
    """
    Get full data regarding one page
    """
    queryset = Page.objects.all()
    serializer_class = PageFullSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(creator=self.request.user, pk=self.kwargs['pk'])
