from django.test import TestCase
# Create your tests here.
from django.urls import resolve

#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.models import User
from .views import home,board_topics,new_topic
from .models import Board,Topic,Post

class HomeTests(TestCase):
	def setUp(self):
		self.board=Board.objects.create(name='Django',description='Django board.')

		#User.objects.create_user(username='john',email='john@doe.com',password='123')
		url=reverse('home')
		self.response=self.client.get(url)

	def test_home_view_status_code(self):
		#url=reverse('home')
		#response=self.client.get(url)
		self.assertEquals(self.response.status_code,200)

	def test_home_url_resolves_home_view(self):
		view=resolve('/')
		self.assertEquals(view.func,home)

	def test_home_view_contains_link_to_topics_page(self):
		board_topics_url=reverse('board_topics',kwargs={'pk':self.board.pk})
		self.assertContains(self.response,'href="{0}"'.format(board_topics_url))

class  BoardTopicsTests(TestCase):
	#creates an instance of 'Board' and 'User' to use in the tests since the django testting suite doesn't run tests against the current database.
	def setUp(self):
		Board.objects.create(name='Django',description='Django board')
    	
	
	#checks if Django is returning a status code 200(success) for an existing Board
	def test_board_topics_view_success_status_code(self):
		url=reverse('board_topics',kwargs={'pk':1})
		response =self.client.get(url)
		self.assertEquals(response.status_code,200)

	#checks if Django is returning a status code 404(page not found) for a db that doesn't exist in the database
	def test_board_topics_view_not_found_status_code(self):
		url = reverse('board_topics',kwargs={'pk':99})
		response=self.client.get(url)
		self.assertEquals(response.status_code,404)

	#checks if Django is using the correct view function to render the topics
	def  test_board_topics_url_resolves_board_topics_view(self):
		view=resolve('/boards/1/')
		self.assertEquals(view.func,board_topics)

	def test_board_topics_view_contains_link_back_to_homepage(self):
		board_topics_url=reverse('board_topics',kwargs={'pk':1})
		response=self.client.get(board_topics_url)
		homepage_url=reverse('home')
		self.assertContains(response,'href="{0}"'.format(homepage_url))

	def test_board_topic_view_contains_navigation_links(self):
		board_topics_url=reverse('board_topics',kwargs={'pk':1})
		homepage_url=reverse('home')
		new_topic_url=reverse('new_topic',kwargs={'pk':1})

		response=self.client.get(board_topics_url)

		self.assertContains(response,'href="{0}"'.format(homepage_url))
		self.assertContains(response,'href="{0}"'.format(new_topic_url))

	
class  NewTopicTests(TestCase):
	def setUp(self):
		Board.objects.create(name='Django',description='Django board.')
		User.objects.create_user(username='john',email='john@doe.com',password='123')

	def test_new_topic_view_success_status_code(self):
		url= reverse('new_topic', kwargs={'pk':1})
		response=self.client.get(url)
		self.assertEquals(response.status_code,200)

	def test_new_topic_view_not_found_status_code(self):
		url=reverse('new_topic',kwargs={'pk':99})
		response=self.client.get(url)
		self.assertEquals(response.status_code,404)

	def  test_new_topic_url_resolves_new_topic_view(self):
		view=resolve('/boards/1/new')
		self.assertEquals(view.func,new_topic)

	def test_new_topic_contains_link_back_to_board_topics_view(self):
		new_topic_url=reverse('new_topic',kwargs={'pk':1})
		board_topics_url=reverse('board_topics',kwargs={'pk':1})
		response=self.client.get(new_topic_url)
		self.assertContains(response,'href="{0}"'.format(board_topics_url))
		
    

    #ensures that HTML contains a token
	def test_csrf(self):
		url=reverse('new_topic',kwargs={'pk':1})
		response=self.client.get(url)
		self.assertContains(response,'csrfmiddlewaretoken')

	#sends a valid combination of data and check if the view created a Topic instance and a Post instance
	def test_new_topic_valid_post_data(self):
		url=reverse('new_topic',kwargs={'pk':1})
		data={
			'subject':'Test title',
			'message': 'Lorem ipsum dolor sit amet'
		}
		response=self.client.post(url,data)
		self.assertTrue(Topic.objects.exists())
		self.assertTrue(Post.objects.exists())

	#sends an empty dictionary to check how the application is behaving
	def test_new_topic_invalid_post_data(self):
		'''
		Invalid post data should not redirect
		THe expected behavior is to show the fom again with validatoon errors
		'''
		url=reverse('new_topic',kwargs={'pk':1})
		response=self.client.post(url,{})
		self.assertEquals(response.status_code,200)

	#similar to the above test but this time we are sending data.The app is expcted to validate and reject empty subject and message 
	def test_new_topic_invalid_post_data_empty_fields(self):
		'''
		Invalid post should not redirect
		The expected behaviour is to show the form again with validation errors
		''' 
		url=reverse('new_topic',kwargs={'pk':1})
		data={
			'subject':'',
			'message':''	
		}
		response=self.client.post(url,data)
		self.assertEquals(response.status_code,200)
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())