```shell
openssl genrsa -out jwt-private.pem 2048
```

```shell
openssl rsa -in jwt-public.pem -outform PEM -pubout -out jwt-public.pem
```
