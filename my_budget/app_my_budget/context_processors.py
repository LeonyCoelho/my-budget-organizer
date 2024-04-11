from .models import GlobalSettings

def global_currency(request):
    global_settings = GlobalSettings.objects.first()
    currency = global_settings.currency if global_settings else 'BRL'  # Moeda padrão se não houver configurações globais
    return {'global_currency': currency}
