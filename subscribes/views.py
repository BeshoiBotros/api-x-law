from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from . import models
from XLaw import shortcuts
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from XLaw import settings

class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            subscribe_instance = shortcuts.object_is_exist(pk, models.Subscribe, "subscribe not found")
            if subscribe_instance.is_active:
                subscribe_serializer = serializers.SubscribeSerializer(subscribe_instance)
                return Response(subscribe_serializer.data, status=status.HTTP_200_OK)
        subscribe_queryset = models.Subscribe.objects.filter(is_active=True)
        subscribe_serializer = serializers.SubscribeSerializer(subscribe_queryset, many=True)
        return Response(subscribe_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        can_add = shortcuts.check_permission('add_subscribe', request)
        if can_add:
            serializer = serializers.SubscribeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribe', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            serializer = serializers.SubscribeSerializer(instance=instance,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribe', request)
        if can_delete:
            instance = shortcuts.object_is_exist(pk, models.Subscribe, "Subscribe not found.")
            instance.delete()
        else:
            return Response({'message'  : 'you can not perform this action.'}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribeorder', request)
        
        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            if can_view or (instance.companyuser.pk == request.user.pk):
                serialzier = serializers.SubscribeOrderSerializer(instance)
            else:
                return Response({'message':'you do not have access to perform that action'})
        else:
            if can_view:
                queryset = models.SubscribeOrder.objects.all()
                serialzier = serializers.SubscribeOrderSerializer(queryset, many=True)
            else:
                queryset = models.SubscribeOrder.objects.filter(companyuser = request.user)
                serialzier = serializers.SubscribeOrderSerializer(queryset, many=True)
        return Response(serialzier.data)
        
    
    def post(self, request):
        if request.user.is_lawyer:
            serializer_data = request.data.copy()
            serializer_data['companyuser'] = request.user
            serializer = serializers.SubscribeOrderSerializer(data=serializer_data)
            validate_data = serializer.validated_data
            if serializer.is_valid():
                instance = serializer.save()
                send_mail(
                    "subscribe order",
                    "your order is underprocess we will check your data then asking you to complate the contract or cancel it",
                    settings.XLAW_EMAIL,
                    [request.user.email],
                    fail_silently=False,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : 'Only lawyers can perform this action.'})
        
    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribeorder', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
            serializer = serializers.SubscribeOrderSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if instance.requestStatus == "accepted":
                    subscribe_contract_data = {'subscribe_order' : instance.subscribe}
                    subscribe_contract_serializer = serializers.SubscribeContractSerializer(data=subscribe_contract_data)
                    if subscribe_contract_serializer.is_valid():
                        serializer.save()
                        send_mail(
                            "subscribe order",
                            "your subscribe order has been successfully accepted, please come to us to complate the contract",
                            settings.XLAW_EMAIL,
                            [instance.companyuser.email],
                            fail_silently=False,
                        )
                if instance.requestStatus == "rejected" or instance.requestStatus == "other":
                    send_mail(
                        "subscribe order",
                        "your subscribe order has been rejected, please check the description of subscribe order to know details.",
                        settings.XLAW_EMAIL,
                        [instance.companyuser.email],
                        fail_silently=False,
                    )

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        # to cancel the subscribe order
        instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeOrder)
        if instance.companyuser.pk == request.user.pk:
            instance.requestStatus = "canceled"
            instance.save()
            send_mail(
                "subscribe order",
                "your subscribe order has been canceled",
                settings.XLAW_EMAIL,
                [instance.companyuser.email],
                fail_silently=False,
            )
            return Response({'message' : 'subscribe order has been canceled successfuly'}, status=status.HTTP_200_OK)
        else:
            can_delete = shortcuts.check_permission('delete_subscribeorder', request)
            if can_delete:
                instance.requestStatus = "canceled"
                instance.save()
                send_mail(
                    "subscribe order",
                    "your subscribe order has been canceled",
                    settings.XLAW_EMAIL,
                    [instance.companyuser.email],
                    fail_silently=False,
                )
                return Response({'message' : 'subscribe order has been canceled successfuly'}, status=status.HTTP_200_OK)
            else:
                return Response({'message' : 'you can only cancel your subscribe orders.'})

class SubscribeContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribecontract', request)
        if pk:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            if can_view or (instance.subscribe_order.companyuser.pk == request.user.pk):
                serialzier = serializers.SubscribeContractSerializer(instance)
            else:
                return Response({'message': 'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            if can_view:
                queryset = models.SubscribeContract.objects.all()
                serialzier = serializers.SubscribeContractSerializer(queryset, many=True)
                return Response(serialzier.data, status=status.HTTP_200_OK)
            else:
                queryset = models.SubscribeContract.objects.filter(subscribe_order__companyuser__id=request.user.pk)
                serializer = serializers.SubscribeContractSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
    # def post(self, request):
    #     can_add = shortcuts.check_permission('add_subscribecontract', request)
    #     if can_add:
    #         serializer = serializers.SubscribeContractSerializer(data=request.data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             company_user_email = instance.subscribe_order.companyuser.email
    #             # need to complate ----------------------------------------------------------------
    #             print(company_user_email)
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'message': 'you do not have access to perform that action'})

    def patch(self, request, pk):
        can_update = shortcuts.check_permission('change_subscribecontract', request)
        if can_update:
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            serializer = serializers.SubscribeContractSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (instance.subscribe_contract_status == "paied") and (instance.is_active == True) or (instance.is_active == True):
                    send_mail(
                        "subscribe contract",
                        "your subscribe order has been successfully accepted, please check the description of subscribe contract to know details.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                if instance.subscribe_contract_status == "rejected" or instance.subscribe_contract_status == "other":
                    send_mail(
                        "subscribe contract",
                        "your subscribe contract has been rejected, please check the description  of subscribe contract to know details.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                if instance.subscribe_contract_status == "unpaied":
                    send_mail(
                        "subscribe contract",
                        "your subscribe contract is unpaid, please make sure to paid then upload the reciept file to activate your Organization.",
                        settings.XLAW_EMAIL,
                        [instance.subscribe_order.companyuser.email],
                        fail_silently=False,
                    )
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'you do not have access to perform that action'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        can_delete = shortcuts.check_permission('delete_subscribecontract', request)
        if can_delete or (instance.subscribe_order.companyuser.pk == request.user.pk):
            instance = shortcuts.object_is_exist(pk=pk, model=models.SubscribeContract)
            instance.subscribe_contract_status = 'canceled'
            instance.save()
            send_mail(
                "subscribe contract",
                "your subscribe contract has been canceled",
                settings.XLAW_EMAIL,
                [instance.subscribe_order.companyuser.email],
                fail_silently=False,
            )
            return Response({'message': 'subscribe contract has been canceled successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'you can only cancel your contracts.'}, status=status.HTTP_400_BAD_REQUEST)
        

class SubscribeContractDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        can_view = shortcuts.check_permission('view_subscribecontractdetails', request)
        if pk:
            instance = shortcuts.object_is_exist(pk, models.SubscribeContractDetails, "subscribe contract details not found")
            if can_view or (instance.subscribe_contract.subscribe_order.companyuser.pk == request.user.pk):
                pass
            else:
                return Response({'message' : 'only admins and contract owners can view this.'})
        else:
            if can_view:
                queryset = models.SubscribeContractDetails.objects.all()
                serializer = serializers.SubscribeContractDetailsSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                queryset = models.SubscribeContractDetails.objects.filter(subscribe_contract__subscribe_order__companyuser__pk = request.user.pk)
                

    def post(self, request):
        pass

    def patch(self, request, pk):
        pass

    def delete(self, request, pk):
        pass