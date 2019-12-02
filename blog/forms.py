from django import forms
from .models import Blog,Comment

banned_email_list = ["ahmet@gmail.com","deneme@carpeu.com","ramosvaldo9@gmail.com"]

class Iletisim_Form(forms.Form):
    isim = forms.CharField(widget=forms.TextInput(attrs = {"class":"form-control"}),max_length=50,label="İsim",required=False)
    soyisim = forms.CharField(max_length=50,label="Soyisim",required=False)
    email = forms.EmailField(max_length=60,label="Email",required=True)
    email2 = forms.EmailField(max_length=50,label="Email Kontrol",required=True)
    icerik = forms.CharField(max_length=1000,label="İçerik")

    def __init__(self,*args,**kwargs):
        super(Iletisim_Form,self,).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class" : "form-control"}
        self.fields["icerik"].widget = forms.Textarea(attrs = {"class" :"form-control"}),
        #self.fields["icerik"] = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))

    def clean_isim(self):
        isim = self.cleaned_data.get("isim")
        if isim == "ahmet":
            raise forms.ValidationError("lütfen ahmet dışında bir kullanıcı giriş yapsın")
        return isim

    def clean_email(self):
        email = self.cleaned_data.get("email")
        isim = self.cleaned_data.get("isim")
        if email in banned_email_list:
            raise forms.ValidationError("lütfen ban yememiş bir mail adresiyle devam ediniz.")
        return email

    def clean(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email != email2:
            self.add_error("email","Emailler eşleşmedi")
            self.add_error("email2","Emailler eşleşmedi")
            #raise forms.ValidationError("Emailler eşleşmedi.")


class Blog_Form(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ["title","image","content","yayin_taslak","kategoriler"]

    def __init__(self,*args,**kwargs):
        super(Blog_Form, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {"class" : "form-control"}
        self.fields["content"].widget.attrs["rows"] = 10
        #self.fields["content"].widget.attrs = {"rows":10, "class": "form-control"}

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 100:
            uzunluk = len(content)
            msg = "Lütfen en az 250 karakter giriniz. Girilen karakter sayısı (%s)" %(uzunluk)
            raise forms.ValidationError(msg)
        return content

class PostSorguForm(forms.Form):
    YAYIN_TASLAK = (("all","HEPSİ"),("yayin","YAYIN"),("taslak","TASLAK"))

    search = forms.CharField(required = False, max_length = 500,widget = forms.TextInput(attrs ={'placeholder':'Bir şeyler arayınız','class':'form-control'}))
    taslak_yayin = forms.ChoiceField(label = '',widget = forms.Select(attrs = {'class':'form-control'}),choices = YAYIN_TASLAK,required = False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["icerik"]

    def __init__(self,*args,**kwargs):
        super(CommentForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': "form-control"}