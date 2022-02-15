from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Tweet, TweetComment
from django.views.generic import ListView, TemplateView


# Create your views here.
def home(request):
    user = request.user.is_authenticated # 사용자가 로그인 했는지 확인
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


@login_required
def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            all_tweet = Tweet.objects.all().order_by('-created_at') # 생성 시간 역순
            return render(request, 'tweet/home.html', {'tweet': all_tweet})
        else:
            return redirect('/sign-in')

    elif request.method == 'POST':
        user = request.user
        content = request.POST.get('my-content', '')
        tags = request.POST.get('tag', '').split(',')

        if content == '':
            all_tweet = Tweet.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html', {'error': '빈칸을 채워주세요!', 'tweet': all_tweet})
        else:
            my_tweet = Tweet.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


@login_required
def delete_tweet(request, id):
    my_tweet = Tweet.objects.get(id=id)
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    if request.method == 'GET':
        cur_tw = Tweet.objects.get(id=id)
        tw_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
        return render(request, 'tweet/tweet_detail.html', {'tweet': cur_tw, 'comment': tw_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '')
        cur_tw = Tweet.objects.get(id=id)

        tc = TweetComment()
        tc.comment = comment
        tc.author = request.user
        tc.tweet = cur_tw
        tc.save()
        return redirect('/tweet/' + str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    cur_tw_id = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(cur_tw_id))


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = Tweet

    def get_queryset(self):
        return Tweet.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'
