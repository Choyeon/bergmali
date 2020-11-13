import mistune
from django.contrib.auth import get_user_model
from django.db import models

from django.utils.functional import cached_property

User = get_user_model()

"""
on_delete 参数选项
CASCADE:这就是默认的选项，级联删除，你无需显性指定它。
PROTECT: 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误。
SET_NULL: 置空模式，删除的时候，外键字段被设置为空，前提就是blank=True, null=True,定义该字段的时候，允许为空。
SET_DEFAULT: 置默认值，删除的时候，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。
SET(): 自定义一个值，该值当然只能是对应的实体了
"""


class Category(models.Model):
    """
    这是分类的ORM模型类
    """
    STATUS_NORMAL = 1  # 正常状态
    STATUS_DELETE = 0  # 删除状态
    # 状态项目
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    # 分类名称
    name = models.CharField(max_length=50, verbose_name="名称")
    # 分类状态
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    # 是否是导航
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    # 作者的外键定义 指向'User'模型类 如果原作者被删除 则作者为空
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE, related_name='category')
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        category = cls.objects.filter(status=cls.STATUS_NORMAL)
        navigation = []
        categories = []
        for cate in category:
            if cate.is_nav:
                navigation.append(cate)
            else:
                categories.append(cate)
        return {
            'navigation': navigation,
            'categories': categories
        }


class Tag(models.Model):
    """
    标签模型类
    """
    STATUS_NORMAL = 1  # 正常状态
    STATUS_DELETE = 0  # 删除状态
    # 状态项目
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    # 标签名
    name = models.CharField(max_length=10, verbose_name="名称")
    # 标签状态
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    # 作者的外键定义 指向'User'模型类 如果原作者被删除 则作者为空
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE, related_name='tag')
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    文章发布模型类
    """
    STATUS_NORMAL = 1  # 正常状态
    STATUS_DELETE = 0  # 删除状态
    STATUS_DRAFT = 2  # 草稿状态
    # 状态项目
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿')
    )
    # 文章标题
    title = models.CharField(max_length=255, verbose_name="标题")
    # 文章摘要
    desc = models.CharField(max_length=1024, verbose_name="摘要")
    # 文章正文
    content = models.TextField(verbose_name='正文', help_text='正文必须为Markdown格式')
    content_html = models.TextField(verbose_name='正文HTML部分', blank=True, editable=False)
    # 文章状态
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    # 文章的分类
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE, related_name="article")
    # 文章的标签 多对多
    tag = models.ManyToManyField(Tag, verbose_name="标签", related_name='article')
    # 文章的作者
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE, related_name='article')
    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 是否是MarkDown
    is_md = models.BooleanField(default=False, verbose_name='Markdown语法')
    # 来源
    source = models.CharField(max_length=200, verbose_name='来源', default='原创')

    # 文章访问量
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']

    def __str__(self):
        return self.title

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    @staticmethod
    # 黑箱格式化获取标签
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')

        return post_list, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related("owner", "category")

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    def save(self, *args, **kwargs):
        if self.is_md:
            self.content_html = mistune.markdown(self.content)
        else:
            self.content_html = self.content
        super().save(*args, **kwargs)

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))
