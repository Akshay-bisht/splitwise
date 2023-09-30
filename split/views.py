from rest_framework.views import APIView
from split.serializers import UserSerializer,ExpenseSerializer,ExpenseShareSerializer,UserBalancesSerializer,UserPassbookSerializer
from rest_framework import status
from rest_framework.response import Response
from split.models import User, Expense
from django.shortcuts import get_object_or_404
from rest_framework import generics
from django.db import transaction
from split.exceptions import AmountSumMismatchError
# Create your views here.

class UserCreate(APIView):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, format='json'):
        dict = request.data.copy()
        dict['username'] = request.data.get('username', '').lower()
        dict['email'] = request.data.get('email', '').lower()
        serializer = self.serializer_class(data=dict)
        if serializer.is_valid():
            user = serializer.save()
            p = request.data.get('password')
            if p:
                user.set_password(p)
                user.is_active = True
                user.save()
                return Response({"message": "USER_CREATED_SUCCESS"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"password": ["This field is required"]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ExpenseListView(APIView):
    serializer_class = ExpenseSerializer

    def post(self,request):
        data = request.data.copy()
        with transaction.atomic():
            serializer= ExpenseSerializer(data=data)
            if serializer.is_valid():
                expense = serializer.save()
                if data['expense_type']=="EQUAL":
                    total = len(data['selected_user'])
                    for i in data['selected_user']:
                        user = get_object_or_404(User, id=i['user_id'])
                        new = {}
                        new["user"]=user.id 
                        new["expense"]=expense.expense_id
                        new["share"]=data['amount']/total
                        serializerex = ExpenseShareSerializer(data = new)
                        if serializerex.is_valid():
                            serializerex.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response("ok")
                elif data['expense_type']=="EXACT":
                    amount_sum = 0
                    for i in data['selected_user']:
                        user = get_object_or_404(User, id=i['user_id'])
                        new = {}
                        new["user"]=user.id 
                        new["expense"]=expense.expense_id
                        new["share"]=i["share"]
                        amount_sum += i["share"]
                        serializerex = ExpenseShareSerializer(data = new)
                        if serializerex.is_valid():
                            serializerex.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    if amount_sum !=data["amount"]:
                        raise AmountSumMismatchError(" total sum of shares is not equal to the total amount")
                    return Response("ko")
                elif data['expense_type']=='PERCENT':
                    percent_sum = 0
                    for i in data['selected_user']:
                        user = get_object_or_404(User, id=i['user_id'])
                        new = {}
                        new["user"]=user.id 
                        new["expense"]=expense.expense_id
                        new["share"]=data["amount"]*i["share"]/100
                        percent_sum +=i["share"]
                        serializerex = ExpenseShareSerializer(data = new)
                        if serializerex.is_valid():
                            serializerex.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    if percent_sum !=100:
                        raise AmountSumMismatchError(" total sum of percent is not equal to the 100")
                    return Response("ko")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBalacesView(APIView):
    serializer_class = UserBalancesSerializer

    def get(self,request):
        balances = request.user.calculate_balances()
        serializer = self.serializer_class({"user_id": request.user.id, "balances": balances})
        return Response(serializer.data)

class UserPassbookView(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = UserPassbookSerializer

    def list(self, request, *args, **kwargs):
        expenses = request.user.get_passbook_entries()
        serializer = self.serializer_class(expenses, many=True)
        return Response(serializer.data)