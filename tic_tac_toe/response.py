import traceback
from rest_framework.response import Response


def api_response(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if res['success']:
                return Response({
                    'data': res.get('data', {}),
                    'success': True,
                    'error': res.get('error', ''),
                }, status=res.get('status', 200))
            else:
                return Response({
                    'data': res.get('data', {}),
                    'success': False,
                    'error': res.get('error', ''),
                }, status=res.get('status', 400))
        except Exception as e:
            return Response({
                'data': {},
                'success': False,
                'error': "Something wrong. Please try again after sometime.\nDev Hint(hidden in production): %s" % str(
                    e),
                'exception': str(e),
                'traceback': traceback.format_exc()
            }, status=500)
    return wrapper
