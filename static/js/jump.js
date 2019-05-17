 $(function jump(){

            //alert(bm);
            $('#test2').on('click', function(){
                var article_name = document.getElementById("art_name").value;
                var bm = encodeURIComponent(article_name);
                bm = decodeURIComponent(bm);
                //var authorName = document.getElementById("author_name").value;
                var articleTitle = document.getElementById("article_title").value;

                // alert(articleTitle);
                layer.open({
                    type: 2,
                    area: ['800px', '600px'],
                    shadeClose: true, //点击遮罩关闭
                    content: '/article/?article_name='+bm+'&articletitle='+articleTitle,
                    end: function () {
                        location.reload();
                    }
                });
            });
            $("a[name='detail']").each(function () {
                var currentEle = $(this);
                currentEle.on('click',function () {
                      layer.open({
                    type: 2,
                    area: ['800px', '600px'],
                    shadeClose: true, //点击遮罩关闭
                    content: '/show_detail/?id='+this.innerText,
                    end: function () {
                        location.reload();
                    }
                });
                })
            })

 });