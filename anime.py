# __author__: Mai feng
# __file_name__: anime.py
# __time__: 2019:01:18:17:01
import requests
from pyquery import PyQuery as pq
class Anime(object):
    def __init__(self, keyword):
        # 用户的关键词
        self.keyword = keyword
        # url
        self.url = 'https://wall.alphacoders.com/search.php?search={keyword}&lang=Chinese'.format(keyword=keyword)
        # base_url 
        self.base_url = 'https://wall.alphacoders.com/'
        # post_url 获取真实链接
        self.post_url = 'https://wall.alphacoders.com/get_download_link.php'
        # 实例 requests.session
        self.s = requests.session()


    def get_img_url(self):
        '''获取url链接
        '''
        try:
            res_url = self.s.get(url=self.url)
            if res_url.status_code == 200:
                doc = pq(res_url.text)
                number = doc('#container_page h1 i').text()
                if number:
                    print('一共搜到了 %s 壁纸' %number)
                    items = doc('.boxgrid a').items()
                    for item in items:
                        url = self.base_url + item.attr('href')
                        self.parse_url(url)
                else:
                    print('没有相应的动漫壁纸...')
                    return None
            else:
                return None
        except Exception as e:
            print('get_img_url->error:', e)
            return None

    def parse_url(self, url):
        '''解析img_url获取下载链接

        '''
        try:
            res_url = self.s.get(url=url)
            if res_url.status_code == 200:
                doc = pq(res_url.text)
                data_id = doc('.download-button').attr('data-id')
                data_type = doc('.download-button').attr('data-type')
                data_server = doc('.download-button').attr('data-server')
                data_user_id = doc('.download-button').attr('data-user-id')
                post_data = {
                    'wallpaper_id':data_id,
                    'type':data_type,
                    'server':data_server,
                    'user_id':data_user_id
                }
                res_url = self.s.post(url=self.post_url, data=post_data)
                if res_url.status_code == 200:
                    print(res_url.text)
                else:
                    return None
            else:
                return None
        except Exception as e:
            print('parse_url->error', e)
        pass

    def run(self):
        '''run的流程
        '''
        self.get_img_url()
        pass


if __name__ == "__main__":
    anime = Anime('约会大作战')
    # anime = Anime('nonono')
    anime.run()