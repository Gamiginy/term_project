from django import forms

from .models import Book, Bid


class SearchAuction(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    price = forms.IntegerField(
        label='価格',
        max_value=9999999,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'style': 'width: 300px'})
    )
    isbn_10 = forms.CharField(
        label='ISBN-10',
        max_length=10,
        min_length=10,
        help_text='入力例：0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_13 = forms.CharField(
        label='ISBN-13',
        max_length=14,
        min_length=14,
        help_text='入力例：012-0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    trade_date = forms.DateTimeField(
        label='受け渡し日時',
        required=False,
        widget=forms.DateTimeInput(attrs={'style': 'width: 300px'})
    )

    field = [title, price, isbn_10, isbn_13, trade_date]


AUCTION_TYPE = (
    ('all', 'すべて'),
    ('now', '開催中オークション'),
    ('end', '終了オークション'),
)


class AuctionManagerForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_10 = forms.CharField(
        label='ISBN-10',
        max_length=10,
        min_length=10,
        help_text='入力例：0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_13 = forms.CharField(
        label='ISBN-13',
        max_length=14,
        min_length=14,
        help_text='入力例：012-0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    auction_type = forms.ChoiceField(
        label='状態',
        widget=forms.RadioSelect,
        choices=AUCTION_TYPE,
        required=False,
    )
    field = [auction_type, title, isbn_10, isbn_13]


class SuccessBidAuctionListForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_10 = forms.CharField(
        label='ISBN-10',
        max_length=10,
        min_length=10,
        help_text='入力例：0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_13 = forms.CharField(
        label='ISBN-13',
        max_length=14,
        min_length=14,
        help_text='入力例：012-0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    field = [title, isbn_10, isbn_13]


class HistoryForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_10 = forms.CharField(
        label='ISBN-10',
        max_length=10,
        min_length=10,
        help_text='入力例：0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_13 = forms.CharField(
        label='ISBN-13',
        max_length=14,
        min_length=14,
        help_text='入力例：012-0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    field = [title, isbn_10, isbn_13]


class CreateAuctionForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title',
            'price',
            'isbn_10',
            'isbn_13',
            'description',
            'trade_place',
            'trade_date',
        )


class CreateBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = (
            'price',
        )
        widgets = (

        )


BID_TYPE = (
    ('all', 'すべて'),
    ('top', 'TOP'),
    ('not-top', 'NOT TOP'),
)


class SearchBidForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    price = forms.IntegerField(
        label='現在価格',
        max_value=9999999,
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={'style': 'width: 300px'})
    )
    isbn_10 = forms.CharField(
        label='ISBN-10',
        max_length=10,
        min_length=10,
        help_text='入力例：0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    isbn_13 = forms.CharField(
        label='ISBN-13',
        max_length=14,
        min_length=14,
        help_text='入力例：012-0123456789',
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 300px'})
    )
    bid_type = forms.ChoiceField(
        label='状態',
        widget=forms.RadioSelect,
        choices=BID_TYPE,
        required=False,
    )
    field = [bid_type, title, isbn_10, isbn_13, price]
