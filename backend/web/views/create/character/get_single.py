from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from web.models.character import Character


class GetSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # get方法传入的参数在request.query_params中；post方法传入的参数在request.data中
            character_id = request.query_params.get('character_id')
            character = Character.objects.get(id=character_id, author__user=request.user)
            return Response({
                'result': 'success',
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                }
            })
        except:
            import traceback
            traceback.print_exc()
            print("!!!!!!!!!!")
            return Response({
                'result': '更新角色失败，请稍后再试'
            })