import redis

class RedisCache(object): 
    
    def __init__(self, host="localhost", port=6379, password=""):
        self.host = host
        self.port = int(port)
        self.password = password
        
        self.redis = redis.StrictRedis(host=self.host, port=self.port, password=self.password, decode_responses=True)
         
    def set(self, variable_name, value): 
        self.redis.set(variable_name, value)
        
    def get(self, variable_name, default_value=None): 
        val = self.redis.get(variable_name)
        if val is None and default_value: 
            self.set(variable_name, default_value)
            val = default_value
        try: 
            val = round(float(val), 2)
            val = int(val)
        except ValueError: 
            pass
        finally:
            return val
        
    def get_float(self, variable_name, default_value=None): 
        val = self.redis.get(variable_name)
        try: 
            val = (float(val))
        except ValueError: 
            pass
        finally:
            return val

