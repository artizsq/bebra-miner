x = {"miners": {
            "Canaan Avalon 841": {
                "pow": 0.000714,
                "count": 10
            }
        }}

print(x["miners"]['Canaan Avalon 841']['pow'] * x["miners"]['Canaan Avalon 841']['count'])