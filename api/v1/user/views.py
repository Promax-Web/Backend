import uuid
from datetime import datetime
from random import random

from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, OTP
from ...utilis.helper import generate_key, code_decoder


class AuthView(GenericAPIView):
    def post(self, request, *args, **kvargs):
        data = request.data
        params = data.get('params')
        method = data.get('method')
        if not method:
            return Response({
                "Error": "method kiritilmagan"
            })

        if params is None:
            return Response({
                "Error": "params kiritilmagan"
            })

        if method == "regis":
            phone = params.get("phone")
            user = User.objects.filter(phone=phone).first()
            if user:
                return Response({
                    "Error": "Bu tel nomer allaqachon bor"
                })

            serializer = self.get_serializer(data=params)
            serializer.is_valid(raise_exception=True)
            user = serializer.create(serializer.data)
            user.set_password(params["password"])
            user.save()

            token = Token()
            token.user = user
            token.save()

        elif method == "login":
            nott = 'phone' if "phone" not in params else "password" if "password" not in params else None
            if nott:
                return Response({
                    "Error": f"{nott} polyasi to'ldirilmagan"

                })

            phone = params.get("phone")
            user = User.objects.filter(phone=phone).first()

            if not user:
                return Response({
                    "Error": "Bunday User topilmadi"
                })
            if not user.check_password(params['password']):
                return Response({
                    "Error": "parol  xato"
                })
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token()
                token.user = user
                token.save()

        elif method == "step.one":
            params = data['params']
            phone = params['phone']
            if not phone:
                return Response({
                    "Error": f"paramsda phone polyasi to'ldirilmagan"
                })

            users = User.objects.filter(phone=params["mobile"]).first() or User.objects.filter(
                phone="+" + params["phone"]
            ).first()
            if users:
                return Response(
                    {
                        'Error': "Bunday mobile allaqachon ro'yxatdan  o'tgan"
                    }, status=status.HTTP_400_BAD_REQUEST
                )

            code = random.randint(10000, 99999)
            key = generate_key(50) + "$" + str(code) + "$" + uuid.uuid1().__str__()
            otp = code_decoder(key)
            # sms = sms_sender(params['mobile'], code)

            # if sms.get('status') != "waiting":
            #     return Response({
            #         "error": "sms xizmatida qandaydir muommo",
            #         "data": sms
            #     })
            root = OTP()
            root.phone = params['phone']
            root.key = otp
            root.save()

            return Response({
                "otp": code,
                "token": root.key
            })
        elif method == "step.two":
            nott = 'otp' if "otp" not in params else "token" if "token" not in params else None
            if nott:
                return Response({
                    "Error": f"params.{nott} polyasi to'ldirilmagan"

                })

            otp = OTP.objects.filter(key=params['token']).first()
            if not otp:
                return Response({
                    "Error": f"Xato Token"
                })

            otp.state = "step_two"
            otp.save()
            now = datetime.datetime.now(datetime.timezone.utc)
            cr = otp.created_at
            if (now - cr).total_seconds() > 120:
                otp.is_expired = True
                otp.save()
                return Response({
                    "Error": f"Kod eskirgan"
                })

            if otp.is_expired:
                return Response({
                    "Error": f"Kod eskirgan"
                })

            otp_key = code_decoder(otp.key, decode=True)
            key = otp_key.split("$")[1]
            if str(key) != str(params['otp']):
                otp.tries += 1
                if otp.tries >= 3:
                    otp.is_expired = True

                otp.save()
                return Response({
                    "Error": "Xato OTP"
                })
            user = User.objects.filter(phone=otp.mobile).first() or User.objects.filter(
                phone="+" + otp.mobile).first()

            otp.state = "confirmed"
            otp.save()
            if user:
                return Response({
                    "is_registered": True
                })
            else:
                return Response({
                    "is_registered": False
                })

        else:
            return Response({
                "Error": "Bunday method yoq"
            })

        return Response({
            "result": {
                "token": token.key,
                "phone": user.phone,
                "name": user.first_name,
            }
        })