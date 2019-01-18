from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone

from .models import Book, Bid, History, Notification
from .forms import (
    SearchAuction,
    CreateAuctionForm,
    CreateBidForm,
    AuctionManagerForm,
    SearchBidForm,
    SuccessBidAuctionListForm,
    HistoryForm
)


class TopView(LoginRequiredMixin, generic.ListView):
    template_name = 'auction/top.html'
    context_object_name = 'auction_list'
    form_class = SearchAuction

    def get_queryset(self):
        results = Book.objects.filter(due_date__gte=timezone.now())

        book_title = self.request.GET.get('title')
        price = self.request.GET.get('price')
        isbn_10 = self.request.GET.get('isbn_10')
        isbn_13 = self.request.GET.get('isbn_13')
        trade_date = self.request.GET.get('trade_date')

        if book_title is not None:
            if book_title is not '':
                results = results.filter(title__icontains=book_title)
        if price is not None:
            if price is not '':
                results = results.filter(price__lte=price)
        if isbn_10 is not None:
            if isbn_10 is not '':
                results = results.filter(isbn_10=isbn_10)
        if isbn_13 is not None:
            if isbn_13 is not '':
                results = results.filter(isbn_13=isbn_13)
        if trade_date is not None:
            if trade_date is not '':
                results = results.filter(trade_date__lt=trade_date)

        return results.order_by('-pub_date')[:30]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class AuctionDetailView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = CreateBidForm
    template_name = 'auction/auction_detail.html'

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.book = Book.objects.get(pk=self.kwargs.get('pk'))

        if bid.price > bid.book.price:
            try:
                if Bid.objects.get(book_id=self.kwargs.get('pk'), account_id=self.request.user.id):
                    existing_bid = Bid.objects.get(book_id=self.kwargs.get('pk'), account_id=self.request.user.id)
                    existing_bid.price = bid.price
                    existing_bid.bid_date = timezone.now()
                    existing_bid.save()
                    book = Book.objects.get(pk=self.kwargs.get('pk'))
                    book.price = existing_bid.price
                    book.top_bid_account_id = self.request.user.id
                    book.save()
            except ObjectDoesNotExist:
                bid.account_id = self.request.user.id
                bid.bid_date = timezone.now()
                bid.save()
                book = Book.objects.get(pk=self.kwargs.get('pk'))
                book.price = bid.price
                book.top_bid_account_id = self.request.user.id
                book.save()

        return redirect('auction:auction_detail', self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        History.objects.create(book_id=book.id, account_id=self.request.user.id, browsed_date=timezone.now())
        context['book'] = book
        context['form'] = self.form_class
        if book.due_date < timezone.now():
            context['to_chat_button'] = True
        return context


class MyAuctionManagerView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'auction_list'
    template_name = 'auction/auction_manager.html'
    form_class = AuctionManagerForm

    def get_queryset(self):
        results = Book.objects.filter(account_id=self.request.user.id)

        book_title = self.request.GET.get('title')
        isbn_10 = self.request.GET.get('isbn_10')
        isbn_13 = self.request.GET.get('isbn_13')
        auction_type = self.request.GET.get('auction_type')

        if book_title is not None:
            if book_title is not '':
                results = results.filter(title__icontains=book_title)
        if isbn_10 is not None:
            if isbn_10 is not '':
                results = results.filter(isbn_10=isbn_10)
        if isbn_13 is not None:
            if isbn_13 is not '':
                results = results.filter(isbn_13=isbn_13)
        if auction_type is not None:
            if auction_type is not '':
                if auction_type == 'now':
                    results = results.filter(due_date__gt=timezone.now())
                if auction_type == 'end':
                    results = results.filter(due_date__lt=timezone.now())

        return results.order_by('-pub_date')[:30]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class MyAuctionEditView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    template_name = 'auction/auction_edit.html'
    fields = ('description',)

    def get_context_data(self, **kwargs):
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        context = super().get_context_data(**kwargs)
        # 削除ボタンを表示させるか
        if book.due_date <= timezone.now():
            context['delete_button'] = False
        else:
            context['delete_button'] = True
        if book.due_date < timezone.now():
            context['to_chat_button'] = True
        return context

    def get_object(self, queryset=None):
        return Book.objects.get(pk=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.save()
        return redirect('auction:auction_edit', self.kwargs.get('pk'))


class MyAuctionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name = 'auction/auction_delete.html'
    success_url = reverse_lazy('auction:auction_manager')

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result


class BidListView(LoginRequiredMixin, generic.ListView):
    model = Bid
    template_name = 'auction/bid_list.html'
    form_class = SearchBidForm
    context_object_name = 'bid_list'

    def get_queryset(self):
        results = Bid.objects.filter(account_id=self.request.user.id, book__due_date__gt=timezone.now())

        book_title = self.request.GET.get('title')
        price = self.request.GET.get('price')
        isbn_10 = self.request.GET.get('isbn_10')
        isbn_13 = self.request.GET.get('isbn_13')
        bid_type = self.request.GET.get('bid_type')

        if book_title is not None:
            if book_title is not '':
                results = results.filter(book__title__icontains=book_title)
        if price is not None:
            if price is not '':
                results = results.filter(price__lte=price)
        if isbn_10 is not None:
            if isbn_10 is not '':
                results = results.filter(book__isbn_10=isbn_10)
        if isbn_13 is not None:
            if isbn_13 is not '':
                results = results.filter(book__isbn_13=isbn_13)
        if bid_type is not None:
            if bid_type is not '':
                if bid_type == 'top':
                    results = results.filter(book__top_bid_account_id=self.request.user.id)
                if bid_type == 'not-top':
                    results = results.exclude(book__top_bid_account_id=self.request.user.id)

        return results.order_by('-bid_date')[:30]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class SuccessBidAuctionListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = 'auction/success_bid_auction_list.html'
    context_object_name = 'success_bid_auction_list'
    form_class = SuccessBidAuctionListForm

    def get_queryset(self):
        results = Book.objects.filter(top_bid_account_id=self.request.user.id, due_date__lte=timezone.now())

        book_title = self.request.GET.get('title')
        isbn_10 = self.request.GET.get('isbn_10')
        isbn_13 = self.request.GET.get('isbn_13')

        if book_title is not None:
            if book_title is not '':
                results = results.filter(title__icontains=book_title)
        if isbn_10 is not None:
            if isbn_10 is not '':
                results = results.filter(isbn_10=isbn_10)
        if isbn_13 is not None:
            if isbn_13 is not '':
                results = results.filter(isbn_13=isbn_13)

        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class HistoryView(LoginRequiredMixin, generic.ListView):
    model = History
    template_name = 'auction/history.html'
    context_object_name = 'history'
    form_class = HistoryForm

    def get_queryset(self):
        results = History.objects.filter(account_id=self.request.user.id, book__due_date__gt=timezone.now())

        book_title = self.request.GET.get('title')
        isbn_10 = self.request.GET.get('isbn_10')
        isbn_13 = self.request.GET.get('isbn_13')

        if book_title is not None:
            if book_title is not '':
                results = results.filter(book__title__icontains=book_title)
        if isbn_10 is not None:
            if isbn_10 is not '':
                results = results.filter(book__isbn_10=isbn_10)
        if isbn_13 is not None:
            if isbn_13 is not '':
                results = results.filter(book__isbn_13=isbn_13)

        return results.order_by('-browsed_date')[:30]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class
        return context


class NotificationView(LoginRequiredMixin, generic.ListView):
    model = Notification
    template_name = 'auction/notification.html'
    context_object_name = 'notification'

    def get_queryset(self):
        results = Notification.objects.all().order_by('-date')[:30]
        return results


class CreateAuctionView(LoginRequiredMixin, generic.CreateView):
    model = Book
    template_name = 'auction/create_auction.html'
    form_class = CreateAuctionForm
    success_url = '/'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.pub_date = timezone.now()
        book.due_date = timezone.now() + timezone.timedelta(minutes=1)
        book.account_id = self.request.user.id
        book.save()
        return redirect('auction:create_auction_comp')


class CreateAuctionCompView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'auction/create_auction_comp.html'
