from ninja import Router
from .schemas import LinkSchema, UpdateLinkSchema
from .models import Links, Clicks
from django.shortcuts import get_object_or_404, redirect
import qrcode
from io import BytesIO
import base64

brevis_router = Router()

@brevis_router.post('create/', response={200: LinkSchema, 409: dict})
def create(request, link_schema: LinkSchema):
  data = link_schema.to_model_data()

  redirect_link = data['redirect_link']
  token = data['token']
  expiration_time = data['expiration_time']
  max_unique_clicks = data['max_unique_clicks']

  if token and Links.objects.filter(token=token).exists():
    return 409, {'error': 'Token already exists'}

  link = Links(**data)
  link.save()

  return 200, LinkSchema.from_model(link)

@brevis_router.get('/{token}', response={200: None, 404: dict})
def redirect_link(request, token):
  link = get_object_or_404(Links, token=token, active=True)

  if link.expired():
    return 404, {'error': 'Link expired'}
  
  unique_clicks = Clicks.objects.filter(link=link).values('ip').distinct().count()

  if link.max_unique_clicks and unique_clicks >= link.max_unique_clicks:
    return 404, {'error': 'Link expired'}

  click = Clicks(
    link=link,
    ip=request.META['REMOTE_ADDR']
  )

  click.save()
  
  return redirect(link.redirect_link)

@brevis_router.put('/{link_id}/', response={200: UpdateLinkSchema, 409: dict})
def update_link(request, link_id: int, link_schema: UpdateLinkSchema):
  link = get_object_or_404(Links, id=link_id)

  data = link_schema.dict()

  token = data['token']
  if token and Links.objects.filter(token=token).exclude(id=link_id).exists():
    return 409, {'error': 'Token already exists'}
  
  for field, value in data.items():
    if value is not None:
      setattr(link, field, value)
  
  link.save()
  return 200, link

@brevis_router.get('stats/{link_id}/', response={200: dict})
def stats(request, link_id: int):
  link = get_object_or_404(Links, id=link_id)
  unique_clicks = Clicks.objects.filter(link=link).values('ip').distinct().count()
  total_clicks = Clicks.objects.filter(link=link).values('ip').count()

  return 200, {'unique_clicks': unique_clicks, 'total_clicks': total_clicks}

def get_api_url(request, token):
  scheme = request.scheme
  host = request.get_host()
  return f"{scheme}://{host}/api/{token }"

@brevis_router.get("qrcode/{link_id}/", response={200: dict})
def get_qrcode(request, link_id: int):
    link = get_object_or_404(Links, id=link_id)
    qr = qrcode.QRCode(
        version=1,  
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10,
        border=4, 
    )
    print(get_api_url(request, link.token))
    qr.add_data(get_api_url(request, link.token))
    qr.make(fit=True)

    content = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(content)

    data = base64.b64encode(content.getvalue()).decode('UTF-8')
    return 200, {'content_image': data}
