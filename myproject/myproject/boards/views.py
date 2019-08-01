from django.shortcuts import redirect,render,get_object_or_404
# Create your views here.
from django.contrib.auth.models import User
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from .forms import NewTopicForm
def home(request):
	boards=Board.objects.all()
	return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
	board=get_object_or_404(Board,pk=pk)
	return render(request,'topics.html',{'board':board})

def  new_topic(request,pk):
	board=get_object_or_404(Board,pk=pk)
	user=User.objects.first()

	if request.method=='POST':
		form=NewTopicForm(request.POST)#initiating a form instance
		if form.is_valid():#django checks the validity of the form 
			topic=form.save(commit=False)#saves data in the database
			topic.board=board
			topic.starter=user
			topic.save()
			post=Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=user
				)
			return redirect('board_topics',pk=board.pk)
	else:
			form=NewTopicForm()
	return render(request,'new_topic.html',{'board':board,'form':form})

	# 	subject=request.POST['subject']
	# 	message=request.POST['message']

	# 	user=User.objects.first()#TODO:get the currently logged in user

	# 	topic=Topic.objects.create(
	# 		subject=subject,
	# 		board=board,
	# 		starter=user
	# 		)

	# 	post=Post.objects.create(
	# 		message=message,
	# 		topic=topic,
	# 		created_by=user
	# 		)

	# 	return redirect('board_topics',pk=board.pk)#TODO:redirect to the created topic page

	# return render(request,'new_topic.html',{'board':board})


	# return render(request,'new_topic.html',{'board':board})
	# # boards=Board.objects.all()
	# # boards_names=list()

	# # for board in boards:
	# # 	boards_names.append(board.name)

	# # 	response_html='<br>'.join(boards_names)


	# # return HttpResponse(response_html) 

