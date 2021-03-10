from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from .forms import *
# Create your views here.

def home(request):

    poll = Poll.objects.all()
    paginator = Paginator(poll,15)
    page = request.GET.get('page')
    
    poll = paginator.get_page(page)

    index = poll.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get our new page range. In the latest versions of Django page_range returns 
    # an iterator. Thus pass it to list, to make our slice possible again.
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request,'home.html',{'poll':poll,'page_range':page_range,})

@login_required(login_url='login')
def AddPoll(request):

    # if request.method == 'POST':

    #     question = request.POST['question']
    #     option1 = request.POST['option1']
    #     option2 = request.POST['option2']
    #     option3 = request.POST['option3']
    #     option1photo = request.POST=['option1photo']
    #     option2photo = request.POST=['option2photo']
    #     option3photo = request.POST=['option3photo']

    #     poll = Poll.objects.create(
    #         Question = question,
    #         created_by = request.user,
    #     )
    #     polloptions = PollOptions.objects.create(
    #         poll = poll,
    #         option1 = option1,
    #         option2 = option2,
    #         option3 = option3,
    #         option1photo = option1photo,
    #         option2photo = option2photo,
    #         option3photo = option3photo
    #     )
    #     return redirect('home')

    polloptions_form = AddpollForm()
    poll_form = QuestionForm()
    if request.method == 'POST':
        poll_form = QuestionForm(request.POST)
        polloptions_form = AddpollForm(request.POST,request.FILES)
        if polloptions_form.is_valid() and poll_form.is_valid():
            poll = poll_form.save(commit=False)
            polloptions = polloptions_form.save(commit=False)
            
            polloptions.poll = poll
            poll.created_by = request.user

            poll = poll_form.save(commit=True)
            polloptions = polloptions_form.save(commit=True)

            return redirect('home')

    return render(request,'addpoll.html',{'polloptions_form':polloptions_form,'poll_form':poll_form})

@login_required(login_url='login')
def polls(request,poll_id):
    try:
        polls = get_object_or_404(Poll,pk=poll_id)
        polloptions = PollOptions.objects.all()
        user = User.objects.get(id = request.user.id)
        if request.method == 'POST':
            selected_option = request.POST['poll_option']

            try:
                if selected_option == 'option1':
                        user = User.objects.get(id = request.user.id)
                        polloptionsPk = PollOptions.objects.get(poll=poll_id)
                        vote = Voter.objects.create(
                            voter = user,
                            option = polloptionsPk
                        )
                        polloptionsPk.option1count +=1
                        polloptionsPk.save()

                elif selected_option == 'option2':
                        user = User.objects.get(id = request.user.id)
                        polloptionsPk = PollOptions.objects.get(poll=poll_id)
                        vote = Voter.objects.create(
                            voter = user,
                            option = polloptionsPk
                        )

                        polloptionsPk.option2count +=1
                        polloptionsPk.save()

                elif selected_option == 'option3':
                        user = User.objects.get(id = request.user.id)
                        polloptionsPk = PollOptions.objects.get(poll=poll_id)
                        vote = Voter.objects.create(
                            voter = user,
                            option = polloptionsPk
                        )

                        polloptionsPk.option3count +=1
                        polloptionsPk.save()
            except IntegrityError:
                messages.error(request,'You Already Voted!')
                return redirect('polls',polls.pk)

            

            return redirect('result',polls.pk)
    except MultiValueDictKeyError:
        messages.info(request,'You Have To Vote!')
        return redirect('polls',polls.pk)

    return render(request,'polls.html',{'polls':polls})


@login_required(login_url='login')
def PollQuestionEdit(request,poll_id):

    # poll = get_object_or_404(Poll,pk=poll_id)
    # polloptionsPk = PollOptions.objects.get(poll=poll_id)

    # if request.user == poll.created_by:
    #     if request.method == 'POST':
    #         question = request.POST['question']
    #         option1 = request.POST['Option1']
    #         option2 = request.POST['Option2']
    #         option3 = request.POST['Option3']

    #         poll.Question = question
    #         polloptionsPk.option1 = option1
    #         polloptionsPk.option2 = option2
    #         polloptionsPk.option3 = option3
    #         poll.save()
    #         polloptionsPk.save()
    #         return redirect('home')
    #     return render(request,'question_edit.html',{'poll':poll})
    # else:
    #     return redirect('home')

    poll = get_object_or_404(Poll,pk=poll_id)
    polloptionsPk = PollOptions.objects.get(poll=poll_id)

    poll_form = QuestionForm(instance=poll)
    polloptions_form = AddpollForm(instance=polloptionsPk)
    if request.method == 'POST':
        poll_form = QuestionForm(request.POST,instance=poll)
        polloptions_form = AddpollForm(request.POST,request.FILES,instance=polloptionsPk)

        if poll_form.is_valid() and polloptions_form.is_valid():
            poll_form.save()
            polloptions_form.save()
            return redirect('home')
    
    return render(request,'question_edit.html',{'poll_form':poll_form,'polloptions_form':polloptions_form,'polloptions':polloptionsPk})


@login_required(login_url='login')
def PollDelete(request,poll_id):

    poll = get_object_or_404(Poll,pk=poll_id)
    if request.user == poll.created_by:
        if request.method == 'POST':
            Poll.objects.get(pk=poll_id).delete()
            return redirect('home')
        return render(request,'poll_delete.html',{'poll':poll})
    else:
        return redirect('home')

def result(request,poll_id):

    polls = get_object_or_404(Poll,pk=poll_id)
    return render(request,'result.html',{'polls':polls})

