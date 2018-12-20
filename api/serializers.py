from rest_framework import serializers
from items.models import Item, FavoriteItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model= User
		fields= ['first_name', 'last_name']

class FavSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model= FavoriteItem
		fields= ['user']

class ItemListSerializer(serializers.ModelSerializer):
	added_by= UserSerializer()
	detail = serializers.HyperlinkedIdentityField(
		view_name = "detail",
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	fav_by= serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ['name', 'image','added_by', 'detail', 'fav_by']

	def get_fav_by(self, obj):
		favs= FavoriteItem.objects.filter(item=obj)
		return favs.count()


class ItemDetailSerializer(serializers.ModelSerializer):
	fav_by= serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ['name', 'image', 'description', 'fav_by']
	def get_fav_by(self, obj):
		return FavSerializer(obj.favoriteitem_set.all(), many=True).data

