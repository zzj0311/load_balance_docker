# load_balance_docker
Use nginx to transfer all income data pack, only suitable for arukas.io

Recently, l found that the ssserver on the arukas.io has such a low latency which pushes me to make full use of it. At the begining, just used a provided host to stream the data to achieve a static url & port. Then, it appears that it's bw is so poor and that leads to this simple docker image.

What this image does is just to transfer all income data to the ssserver docker, so actually you can use this image to do all the transfer work within arukas.io, hope useful.

There's four ENV varibles supported:
* **API_KEY**: means you should give it the right arukas.io api key to work;
* **API_PASS**: similarly, should provide the matched api pass;
* **CONTAINER**: the target container id;
* **INTERVAL**: the interval to check instance ip & port

So, that's it. Have a good day:)
Be free to contact me at support@mail.zzzzzzj.me & if you found it useful, it's nice of you to buy me a cup of coffee XD
![Alipay](https://blog.zzzzzzj.me/content/images/2017/04/Screenshot_20170401-215654.png)
