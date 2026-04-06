<template>
  <div class="learning-page">
    <HeroSection />
    <LevelTabs v-model="currentLevel" />

    <ToolSection
      :level="currentLevel"
      :filteredTools="filteredTools"
      :animals="animals"
      :plants="plants"
      :seasons="seasons"
      :solarTerms="solarTerms"
      :regions="regions"
      :advancedItems="advancedItems"
      :currentTool="currentTool"
      :showDetail="showDetail"
      :currentPage="currentPage"
      @selectTool="selectTool"
      @toggleDetail="toggleDetail"
      @askToolMore="askToolMore"
      @changePage="handlePageChange"
      @enterModule="enterModule"
    />

  

   <!-- ================== 视频推荐 ================== -->
    <div class="page-block">
      <VideoSection />
    </div>
      
    <div class="page-block">
      <AIBox
        :messages="messages"
        :input="input"
        :isTyping="isTyping"
        :chatListRef="chatListRef"
        :renderMarkdown="renderMarkdown"
        @sendMessage="sendMessage"
        @quickAsk="quickAsk"
        @clearChat="clearChat"
        @update:input="val => input = val"
      />
    </div>
  </div>
</template>

<script setup>
import HeroSection from '@/components/learning/HeroSection.vue'
import ToolSection from '@/components/learning/ToolSection.vue'
import VideoSection from '@/components/learning/VideoSection.vue'


import AIBox from '@/components/learning/AIBox.vue'
import { computed, nextTick, ref, onMounted, watch } from 'vue'
import LevelTabs from '../components/learning/LevelTabs.vue'
import chanziImg from '@/assets/tools/chanzi.png'
import chutouImg from '@/assets/tools/chutou.png'
import liandaoImg from '@/assets/tools/liandao.png'
import paziImg from '@/assets/tools/pazi.png'
import penhuImg from '@/assets/tools/penhu.png'
import tieqiuImg from '@/assets/tools/tieqiu.png'


import ciweiImg from '@/assets/animals/ciwei.png'
import mifengImg from '@/assets/animals/mifeng.png'
import piaochongImg from '@/assets/animals/piaochong.png'
import qingwaImg from '@/assets/animals/qingwa.png'
import qiuyinImg from '@/assets/animals/qiuyin.png'
import xiaojiImg from '@/assets/animals/xiaoji.png'


import damaiImg from '@/assets/plants/damai.png'
import gaoliangImg from '@/assets/plants/gaoliang.png'
import limaiImg from '@/assets/plants/limai.png'
import qiaomaiImg from '@/assets/plants/qiaomai.png'
import sumiImg from '@/assets/plants/sumi.png'
import shuidaoImg from '@/assets/plants/shuidao.png'
import xiaomaiImg from '@/assets/plants/xiaomai.png'
import xiaomiImg from '@/assets/plants/xiaomi.png'
import yanmaiImg from '@/assets/plants/yanmai.png'
import caomeiImg from '@/assets/plants/caomei.png'
import fanqieImg from '@/assets/plants/fanqie.png'
import tudouImg from '@/assets/plants/tudou.png'
import xiangrikuiImg from '@/assets/plants/xiangrikui.png'
import xiaobaicaiImg from '@/assets/plants/xiaobaicai.png'
import qiushouImg from '@/assets/seasons/qiushou.png'
import dongcangImg from '@/assets/seasons/dongcang.png'
import lichun from '@/assets/solarTerms/lichun.png'
import yushui from '@/assets/solarTerms/yushui.png'
import jingzhe from '@/assets/solarTerms/jingzhe.png'
import chunfen from '@/assets/solarTerms/chunfen.png'
import qingming from '@/assets/solarTerms/qingming.png'
import guyu from '@/assets/solarTerms/guyu.png'

import lixia from '@/assets/solarTerms/lixia.png'
import xiaoman from '@/assets/solarTerms/xiaoman.png'
import mangzhong from '@/assets/solarTerms/mangzhong.png'
import xiazhi from '@/assets/solarTerms/xiazhi.png'
import xiaoshu from '@/assets/solarTerms/xiaoshu.png'
import dashu from '@/assets/solarTerms/dashu.png'

import liqiu from '@/assets/solarTerms/liqiu.png'
import chushu from '@/assets/solarTerms/chushu.png'
import bailu from '@/assets/solarTerms/bailu.png'
import qiufen from '@/assets/solarTerms/qiufen.png'
import hanlu from '@/assets/solarTerms/hanlu.png'
import shuangjiang from '@/assets/solarTerms/shuangjiang.png'

import lidong from '@/assets/solarTerms/lidong.png'
import xiaoxue from '@/assets/solarTerms/xiaoxue.png'
import daxue from '@/assets/solarTerms/daxue.png'
import dongzhi from '@/assets/solarTerms/dongzhi.png'
import xiaohan from '@/assets/solarTerms/xiaohan.png'
import dahan from '@/assets/solarTerms/dahan.png'
import zidonghua from '@/assets/high/zidonghua.png'
import huanjing from '@/assets/high/huanjing.png'
import { useRouter } from 'vue-router'
import dongbei from '@/assets/regions/dongbei.png'
import huabei from '@/assets/regions/huabei.png'
import changjiang from '@/assets/regions/changjiang.png'
import huanan from '@/assets/regions/huanan.png'
import xibei from '@/assets/regions/xibei.png'
import xinan from '@/assets/regions/xinan.png'
const router = useRouter()

const enterModule = (item) => {
  if (item.id === 'a1') router.push('/dashboard')
  if (item.id === 'a2') router.push('/control')
  if (item.id === 'a3') router.push('/dashboard')
}
const currentPage = ref(0)
const currentLevel = ref('primary')

watch(currentLevel, () => {
  currentPage.value = 0
})



const showDetail = ref(false)

const tools = ref([
  {
    id: 1,
    name: '锄头',
    tag: '松土工具',
    level: '入门农具',
    usage: '用来翻松泥土、除掉杂草。',
    detail: '锄头可以让土壤变得松软，帮助植物更好生长，同时还能清理杂草。',
    points: ['松土', '除草', '帮助植物生长'],
    image: chutouImg
  },
  {
    id: 2,
    name: '铁锹',
    tag: '挖掘工具',
    level: '基础农具',
    usage: '用来挖土和搬运泥土。',
    detail: '铁锹适合挖较深的土，比如挖坑种树，是农田常用工具。',
    points: ['挖坑', '搬运泥土', '适合深挖'],
    image: tieqiuImg
  },
  {
    id: 3,
    name: '喷壶',
    tag: '灌溉工具',
    level: '轻便工具',
    usage: '用来给植物浇水。',
    detail: '喷壶水流柔和，适合给幼苗浇水，不会伤害植物。',
    points: ['保护幼苗', '水流柔和', '操作简单'],
    image: penhuImg
  },
  {
    id: 4,
    name: '耙子',
    tag: '整理工具',
    level: '基础农具',
    usage: '用来整理土地，让地面更平整。',
    detail: '耙子可以打碎土块，让土地更适合种植。',
    points: ['平整土地', '打碎土块', '方便播种'],
    image: paziImg
  },
  {
    id: 5,
    name: '铲子',
    tag: '搬运工具',
    level: '基础工具',
    usage: '用来铲土和搬运泥土。',
    detail: '铲子适合把土铲起来移动，是农田常见工具。',
    points: ['铲土', '搬运', '操作简单'],
    image: chanziImg
  },
  {
    id: 6,
    name: '镰刀',
    tag: '收割工具',
    level: '传统农具',
    usage: '用来收割农作物。',
    detail: '镰刀常用于割麦子、稻谷等，是传统农业的重要工具。',
    points: ['收割庄稼', '效率高', '操作简单'],
    image: liandaoImg
  }
])

const animals = ref([
  {
    id: 1,
    name: '蜜蜂',
    tag: '授粉小能手',
    level: '生态伙伴',
    usage: '帮助植物开花结果。',
    detail: '蜜蜂在花之间传播花粉，是农作物结果的重要帮手。',
    points: ['帮助植物结果', '提高产量', '维持生态平衡'],
    image: mifengImg
  },
  {
    id: 2,
    name: '蚯蚓',
    tag: '土壤工程师',
    level: '生态伙伴',
    usage: '让土壤更加松软。',
    detail: '蚯蚓在地下活动，可以让土壤更加透气，帮助植物吸收养分。',
    points: ['改善土壤结构', '增加透气性', '促进植物生长'],
    image: qiuyinImg
  },
  {
    id: 3,
    name: '瓢虫',
    tag: '益虫',
    level: '生态伙伴',
    usage: '帮助消灭害虫。',
    detail: '瓢虫会吃掉农作物上的害虫，是农民的好帮手。',
    points: ['减少害虫', '保护植物', '生态平衡'],
    image: piaochongImg
  },
  {
    id: 4,
    name: '青蛙',
    tag: '捕虫能手',
    level: '生态伙伴',
    usage: '捕食农田害虫。',
    detail: '青蛙会吃掉蚊虫和害虫，帮助保护农作物。',
    points: ['减少虫害', '保护农田', '生态平衡'],
    image: qingwaImg
  },
  {
    id: 5,
    name: '小鸡',
    tag: '农场动物',
    level: '生活伙伴',
    usage: '提供鸡蛋和肉类。',
    detail: '小鸡是农场中常见的动物，也可以帮助吃掉一些小虫。',
    points: ['提供食物', '农场常见', '容易饲养'],
    image: xiaojiImg
  },
  {
    id: 6,
    name: '刺猬',
    tag: '夜间守护者',
    level: '生态伙伴',
    usage: '捕食害虫。',
    detail: '刺猬喜欢在夜间活动，会吃掉害虫，保护农作物。',
    points: ['吃害虫', '保护植物', '生态平衡'],
    image: ciweiImg
  }
])

const plants = ref([
  {
    id: 1,
    name: '水稻',
    tag: '主食作物',
    level: '基础作物',
    usage: '用来生产大米。',
    detail: '水稻需要在水田中生长，是重要粮食。',
    points: ['需要水田', '主食来源', '产量高'],
    image: shuidaoImg
  },
  {
    id: 2,
    name: '小麦',
    tag: '主食作物',
    level: '基础作物',
    usage: '用来制作面粉。',
    detail: '小麦可以做面条、馒头等。',
    points: ['做面粉', '用途广', '重要粮食'],
    image: xiaomaiImg
  },
  {
    id: 3,
    name: '小米',
    tag: '谷物',
    level: '基础作物',
    usage: '可煮粥食用。',
    detail: '小米营养丰富，是传统粮食。',
    points: ['营养高', '易消化', '传统作物'],
    image: xiaomiImg
  },
  {
    id: 4,
    name: '高粱',
    tag: '粮食作物',
    level: '基础作物',
    usage: '可做食物或酿酒。',
    detail: '高粱耐旱，适应能力强。',
    points: ['耐旱', '用途多', '适应性强'],
    image: gaoliangImg
  },
  {
    id: 5,
    name: '大麦',
    tag: '粮食作物',
    level: '基础作物',
    usage: '可做食品或饲料。',
    detail: '大麦也是青稞的一种。',
    points: ['用途广', '耐寒', '可做饲料'],
    image: damaiImg
  },
  {
    id: 6,
    name: '燕麦',
    tag: '健康粮食',
    level: '基础作物',
    usage: '常用于早餐食品。',
    detail: '燕麦富含营养，对身体有益。',
    points: ['营养高', '健康食品', '易种植'],
    image: yanmaiImg
  },
  {
    id: 7,
    name: '荞麦',
    tag: '特色粮食',
    level: '对比作物',
    usage: '可制作荞麦面。',
    detail: '荞麦不属于禾本科。',
    points: ['非禾本科', '营养高', '特色作物'],
    image: qiaomaiImg
  },
  {
    id: 8,
    name: '藜麦',
    tag: '健康粮食',
    level: '对比作物',
    usage: '营养丰富的粮食。',
    detail: '藜麦属于苋科植物。',
    points: ['高蛋白', '非禾本科', '健康食品'],
    image: limaiImg
  },
  {
    id: 9,
    name: '小白菜',
    tag: '蔬菜',
    level: '入门植物',
    usage: '常见蔬菜。',
    detail: '生长快，适合新手种植。',
    points: ['生长快', '容易种', '适合新手'],
    image: xiaobaicaiImg
  },
  {
    id: 10,
    name: '番茄',
    tag: '蔬菜',
    level: '入门植物',
    usage: '可直接食用。',
    detail: '番茄可以在阳台种植。',
    points: ['可结果', '易种植', '营养丰富'],
    image: fanqieImg
  },
  {
    id: 11,
    name: '土豆',
    tag: '块茎作物',
    level: '入门植物',
    usage: '重要食物来源。',
    detail: '土豆在地下生长。',
    points: ['地下生长', '高产', '用途广'],
    image: tudouImg
  },
  {
    id: 12,
    name: '向日葵',
    tag: '观赏植物',
    level: '入门植物',
    usage: '观赏和产葵花籽。',
    detail: '向日葵会随着太阳转动。',
    points: ['向光生长', '观赏性强', '易种植'],
    image: xiangrikuiImg
  },
  {
    id: 13,
    name: '草莓',
    tag: '水果',
    level: '入门植物',
    usage: '可食用水果。',
    detail: '草莓适合家庭种植。',
    points: ['味道甜', '易种植', '孩子喜欢'],
    image: caomeiImg
  }
])

const seasons = ref([
  {
    id: 's1',
    name: '🌸 春耕',
    tag: '3-5月',
    usage: '春季是播种黄金期',
    points: ['水稻、蔬菜', '草莓、樱桃', '立春、清明'],
    image: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=600'
  },
  {
    id: 's2',
    name: '☀ 夏耘',
    tag: '6-8月',
    usage: '作物快速生长',
    points: ['玉米、西瓜', '荔枝、桃子', '芒种、大暑'],
    image: 'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=600'
  },
  {
    id: 's3',
    name: '🍂 秋收',
    tag: '9-11月',
    usage: '收获季节',
    points: ['水稻、大豆', '苹果、柿子', '秋分、霜降'],
    image: qiushouImg   // ✅ 本地图片
  },
  {
    id: 's4',
    name: '❄ 冬藏',
    tag: '12-2月',
    usage: '蓄力阶段',
    points: ['大棚蔬菜', '砂糖橘', '冬至、大寒'],
    image: dongcangImg  // ✅ 本地图片
  }
])



const solarTerms = ref([
  // --- 🌸 春天：唤醒大地的闹钟 ---
  {
    id: 'st1', name: '🌱 立春', tag: '春之序曲', level: '头号玩家',
    usage: '大自然：起床啦！别睡了！',
    detail: '它是春天的“开幕式”。虽然还是很冷，但风里已经有了泥土的香味，冬眠的小懒虫们开始伸懒腰了。',
    points: ['咬春：吃个春饼庆祝一下', '东风开始吹走冰雪', '风筝开始上天啦'],
    image: lichun
  },
  {
    id: 'st2', name: '☔ 雨水', tag: '滋润万物', level: '自然花洒',
    usage: '天空：嘿，送你们一场及时雨。',
    detail: '降雪变成了柔和的雨滴。这不是在下雨，这是大地在喝奶茶，喝饱了植物才能长得更高。',
    points: ['春雨贵如油，别浪费', '草地开始冒出绿绒毛', '大雁从南方飞回来'],
    image: yushui
  },
  {
    id: 'st3', name: '⚡ 惊蛰', tag: '雷鸣行动', level: '唤醒大使',
    usage: '春雷：雷公敲鼓，虫虫起床！',
    detail: '轰隆一声雷，把躲在泥土里睡觉的昆虫全“吓”醒了。大自然的“生物钟”被按下了闹铃。',
    points: ['桃花笑红了脸', '燕子开始找地方筑巢', '害虫也被唤醒了哦'],
    image: jingzhe
  },
  {
    id: 'st4', name: '⚖️ 春分', tag: '昼夜平衡', level: '平衡大师',
    usage: '白天：我和黑夜一人一半！',
    detail: '这一天最公平，白天和黑夜正好一样长。这也是“竖蛋”挑战的最佳时机，你要试试吗？',
    points: ['春祭：去田野里踏青', '挑战：看谁能把鸡蛋立起来', '杨柳垂下长头发'],
    image: chunfen
  },
  {
    id: 'st5', name: '🪁 清明', tag: '气清景明', level: '野外探险',
    usage: '阳光：今天的天空是高清的！',
    detail: '天空蓝得像洗过一样。除了思念祖先，这也是最好的“郊游日”，快去草地上打滚吧。',
    points: ['青团：糯叽叽的春天味道', '插柳：给家门口装点绿色', '微风最适合放风筝'],
    image: qingming
  },
  {
    id: 'st6', name: '🍵 谷雨', tag: '谷物之雨', level: '丰收种子',
    usage: '雨水：让每一颗种子都发芽！',
    detail: '春天的最后一站。这时候的雨水是为了让百谷生长，所以叫“谷雨”，喝杯谷雨茶，神清气爽。',
    points: ['牡丹花：百花之王开了', '樱桃红了，快去采摘', '春耕进入最后的冲刺'],
    image: guyu
  },

  // --- ☀️ 夏天：热情的运动会 ---
  {
    id: 'st7', name: '🍉 立夏', tag: '夏日入场券', level: '派对开始',
    usage: '太阳：我要加大马力了！',
    detail: '夏天的大门打开了！告别春天，穿上短袖，准备迎接蝉鸣和西瓜的季节吧。',
    points: ['立夏蛋：挂在脖子上的玩具', '秤人：看看春天胖了没', '蜻蜓开始在水面点水'],
    image: lixia
  },
  {
    id: 'st8', name: '🌽 小满', tag: '恰到好处', level: '小确幸',
    usage: '庄稼：我吃饱了，正在长肉！',
    detail: '麦子长得越来越饱满，但还没成熟。就像现在的你，充满潜力，正在默默努力成长。',
    points: ['祭蚕：感谢吐丝的小伙伴', '苦菜：忆苦思甜的味道', '田里的水要灌满哦'],
    image: xiaoman
  },
  {
    id: 'st9', name: '🌾 芒种', tag: '忙碌季节', level: '劳动模范',
    usage: '农民伯伯：又收又种，忙翻天！',
    detail: '“芒”是有胡须的麦子，“种”是播种的种子。这是一个边收割边播种的神奇时刻。',
    points: ['煮青梅：酸酸甜甜的夏日', '送花神：明年花会再开', '萤火虫开始提灯巡逻'],
    image: mangzhong
  },
  {
    id: 'st10', name: '🌞 夏至', tag: '漫长的一天', level: '日光领袖',
    usage: '影子：今天我是最短的！',
    detail: '一年中白天最长的一天，晚饭吃完天还是亮的！感觉时间变多了，是不是很赚？',
    points: ['夏至面：冬至饺子夏至面', '避暑：准备好风扇和冰棒', '雷雨：经常会有过云雨'],
    image: xiazhi
  },
  {
    id: 'st11', name: '🍦 小暑', tag: '小热来袭', level: '热身赛',
    usage: '风：吹出来的都是热风。',
    detail: '天气开始变得闷热，大地的每个毛孔都在冒汗。找个树荫坐下，听听蝉叫吧。',
    points: ['晒书：给书本洗个阳光浴', '尝新：吃最新收获的粮食', '温风而至，蟋蟀进屋'],
    image: xiaoshu
  },
  {
    id: 'st12', name: '🔥 大暑', tag: '极热挑战', level: '桑拿房长官',
    usage: '空气：热得冒泡，请避暑！',
    detail: '一年中最热的时候，像待在桑拿房里。虽然很热，但这是作物长得最猛的时候！',
    points: ['伏茶：清热解暑的魔法药水', '萤火虫派对：夜晚最美', '午后雷阵雨是常客'],
    image: dashu
  },

  // --- 🍂 秋天：金色的奖赏 ---
  {
    id: 'st13', name: '🍁 立秋', tag: '秋之信号', level: '凉爽信使',
    usage: '树叶：我也要换个颜色了。',
    detail: '虽然太阳还很猛，但第一片落下的树叶在悄悄告诉你：秋天已经坐上公交车出发了。',
    points: ['贴秋膘：正大光明吃肉', '啃秋：一人抱个大西瓜', '早秋凉意：晚上盖好被子'],
    image: liqiu
  },
  {
    id: 'st14', name: '🌤 处暑', tag: '暑气跑掉', level: '退烧药',
    usage: '暑气：我走啦，大家拜拜！',
    detail: '“处”是终止的意思。这就是暑气打卡下班的日子，凉爽的秋风正式接管大地。',
    points: ['放河灯：思念寄往远方', '开渔节：鱼虾肥美的季节', '早睡早起，身体棒棒'],
    image: chushu
  },
  {
    id: 'st15', name: '🌫 白露', tag: '晶莹剔透', level: '露珠设计师',
    usage: '草地：快看我穿了珍珠衫！',
    detail: '早上的草地上会出现亮晶晶的小水珠，那是大地的项链。气温开始拉开差距了。',
    points: ['白露茶：淡淡的秋香味', '收集露水：古代的小浪漫', '该加衣服啦，别着凉'],
    image: bailu
  },
  {
    id: 'st16', name: '🍂 秋分', tag: '平分秋色', level: '丰收祭司',
    usage: '大自然：一半给黑夜，一半给白天。',
    detail: '第二次昼夜平分。这是一个满地金黄、瓜果飘香的节气，空气里都是甜甜的。',
    points: ['中国农民丰收节', '吃秋菜：身体强壮的秘密', '螃蟹开始横着走啦'],
    image: qiufen
  },
  {
    id: 'st17', name: '🌰 寒露', tag: '寒意初现', level: '冰凉使者',
    usage: '露水：我也想结冰，但再等会。',
    detail: '比起白露，寒露的露水会让你觉得凉飕飕的。菊花在这个时候开得最漂亮。',
    points: ['登高：去山上呼吸凉空气', '赏菊：花丛里的隐士', '石榴红了，籽儿真甜'],
    image: hanlu
  },
  {
    id: 'st18', name: '🌫 霜降', tag: '霜打红叶', level: '调色盘高手',
    usage: '大地：我给自己盖层薄霜。',
    detail: '秋天的最后一位。冷空气把枫叶染得通红，柿子挂在树上像红灯笼一样。',
    points: ['吃柿子：事事如意没商量', '赏红叶：大自然的油画', '寒潮要来啦，秋衣预警'],
    image: shuangjiang
  },

  // --- ❄️ 冬天：宁静的梦境 ---
  {
    id: 'st19', name: '🧣 立冬', tag: '冬之序章', level: '收藏家',
    usage: '万物：关门，冬眠，休息！',
    detail: '冬天的号角响了。辛苦了一年，大自然准备藏起来休息了，你也该多喝热水啦。',
    points: ['补冬：吃顿热腾腾的火锅', '冬泳：勇敢者的游戏', '储存大白菜和土豆'],
    image: lidong
  },
  {
    id: 'st20', name: '❄️ 小雪', tag: '初雪告白', level: '梦幻时刻',
    usage: '雪花：我们先来几个探路。',
    detail: '天空中偶尔会飘下轻盈的雪花，但一落地就化了。虽然还不厚，但很有意境哦。',
    points: ['腌咸菜：冬天的下饭神器', '糍粑：软软糯糯的美味', '开始准备厚棉衣'],
    image: xiaoxue
  },
  {
    id: 'st21', name: '☃️ 大雪', tag: '银装素裹', level: '白雪公主',
    usage: '雪：把世界铺平，晚安。',
    detail: '这时候的雪会下得很大，整个世界都变成了银白色。堆雪人、打雪仗的时刻到了！',
    points: ['打雪仗：冬天最燃的运动', '烤红薯：炉里的香甜回忆', '河流开始结亮晶晶的冰'],
    image: daxue
  },
  {
    id: 'st22', name: '🥟 冬至', tag: '漫长黑夜', level: '暗夜女王',
    usage: '夜晚：我是今天的主角！',
    detail: '白天最短，黑夜最长。过了这一天，白天就开始慢慢变长了。温暖的太阳正在回来。',
    points: ['饺子vs汤圆：南北大战', '数九游戏：九九消寒图', '不吃饺子会冻耳朵哦'],
    image: dongzhi
  },
  {
    id: 'st23', name: '🥶 小寒', tag: '寒冷预警', level: '制冷狂魔',
    usage: '寒风：我要把所有人都吹回家。',
    detail: '别看它叫“小”，其实往往比大寒还冷！记得穿上最厚的那件羽绒服。',
    points: ['腊八粥：暖胃又暖心', '腊梅：雪地里的小香气', '冰上运动：出溜滑走起'],
    image: xiaohan
  },
  {
    id: 'st24', name: '🧧 大寒', tag: '年味终点', level: '守岁官',
    usage: '寒冷：我是最后的关卡！',
    detail: '最后一个节气！虽然冷到极点，但家家户户都在扫房、办年货，新年就要来啦！',
    points: ['大扫除：迎接新的开始', '办年货：快乐买买买', '准备好拿压岁钱了吗'],
    image: dahan
  }
])

const regions = ref([
  {
    id: 'r1',
    name: '🌾 东北农业区',
    tag: '黑龙江 / 吉林 / 辽宁',
    usage: '商品粮基地',
    points: ['玉米','大豆','水稻'],
    image: dongbei
  },
  {
    id: 'r2',
    name: '🌽 华北农业区',
    tag: '河北 / 山东 / 河南',
    usage: '旱作农业区',
    points: ['小麦','玉米','棉花'],
    image: huabei
  },
  {
    id: 'r3',
    name: '🌱 长江中下游农业区',
    tag: '江苏 / 安徽 / 湖北 / 湖南',
    usage: '水田农业发达',
    points: ['水稻','油菜','水产'],
    image: changjiang
  },
  {
    id: 'r4',
    name: '🍊 华南农业区',
    tag: '广东 / 广西 / 福建 / 海南',
    usage: '热带农业',
    points: ['甘蔗','荔枝','香蕉'],
    image: huanan
  },
  {
    id: 'r5',
    name: '🍇 西北农业区',
    tag: '新疆 / 甘肃 / 宁夏',
    usage: '灌溉农业',
    points: ['葡萄','棉花','哈密瓜'],
    image: xibei
  },
  {
    id: 'r6',
    name: '🌸 西南农业区',
    tag: '云南 / 四川 / 贵州',
    usage: '立体农业',
    points: ['茶叶','咖啡','水稻'],
    image: xinan
  }
])


const advancedItems = [
  {
    id: 'env',
    name: ' 环境数据',
    tag: '🌱读懂植物的“语言',
    usage: '传感器是如何感知植物需求的？',
    points: [
      '土壤水分：判定根系是否进入“缺水压力”状态',
      '空气湿度：太高容易诱发霉菌，太低会闭合气孔',
      '光照强度：控制光合作用速率的“燃料”',
      '实时温度：影响酶活性，决定作物的生长速度'
    ],
    
    image: huanjing
  },
  {
    id: 'control',
    name: ' 自动化执行',
    tag: '农场的“钢铁管家”',
    usage: '设备是如何代替汗水实现精准管理的？',
    points: [
      '智能水泵：基于水分阈值，实现“按需滴灌”',
      '光谱补偿灯：模拟太阳光，在阴雨天开启“加班”模式',
      '循环风扇：模拟自然风，增强茎秆强度并降温',
      '自动化遮阳：防止午后强光灼伤幼嫩叶片'
    ],
    
    image: zidonghua
  },
  {
    id: 'data',
    name: '智慧决策',
    tag: '🧠 农业“数字大脑”',
    usage: '数据不只是数字，它是农场的“预言书”',
    points: [
      '生长曲线：预测作物最完美的采摘时刻',
      '病虫害预警：通过温湿度组合，提前拦截灾害',
      '能耗优化：计算最省电的补光与通风方案',
      '历史回溯：总结上一季丰收的“成功密码”'
    ],
    // 建议换一张更有科技质感的、带数据可视化光效的农场图
    image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800'
  }
]
const currentTool = ref(tools.value[0])
const filteredTools = computed(() => tools.value)

const currentVideoUrl = computed(() => {
  return currentTool.value?.videoBvid
    ? `//player.bilibili.com/player.html?bvid=${currentTool.value.videoBvid}&page=1`
    : ''
})

const currentQuiz = ref({
  question: '锄头最常见的用途是什么？',
  options: ['松土除草', '测量温度', '照明田地', '记录产量'],
  answer: '松土除草',
  explanation: '锄头主要用于松土、除草和翻土'
})

const quizAnswered = ref(false)
const isCorrect = ref(false)
const selectedAnswer = ref('')

const checkAnswer = (option) => {
  if (quizAnswered.value) return
  selectedAnswer.value = option
  quizAnswered.value = true
  isCorrect.value = option === currentQuiz.value.answer
}

const resetQuiz = () => {
  quizAnswered.value = false
  isCorrect.value = false
  selectedAnswer.value = ''
}

const getOptionClass = (option) => {
  if (!quizAnswered.value) return ''
  if (option === currentQuiz.value.answer) return 'right-answer'
  if (option === selectedAnswer.value) return 'wrong-answer'
  return ''
}

const selectTool = (item) => {
  currentTool.value = item
  showDetail.value = false
  resetQuiz()
}

const toggleDetail = () => {
  showDetail.value = !showDetail.value
}

const handlePageChange = (page) => {
  currentPage.value = Math.max(0, Math.min(2, page))
}



const input = ref('')
const messages = ref([])
const isTyping = ref(false)
const chatListRef = ref(null)
let messageId = 1

const STORAGE_KEY = 'learning-chat-history'

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) messages.value = JSON.parse(saved)
})

function saveHistory() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages.value))
}

async function callAI(question) {
  try {
    const res = await fetch('http://localhost:8000/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: question })
    })

    const data = await res.json()
    if (data.code === 200) return data.data
    return 'AI返回异常'
  } catch (err) {
    console.error(err)
    return '❌ AI请求失败'
  }
}

const sendMessage = async () => {
  const question = input.value.trim()
  if (!question || isTyping.value) return

  messages.value.push({
    id: messageId++,
    role: 'user',
    content: question
  })

  input.value = ''
  await scrollChatToBottom()

  const aiMessage = {
    id: messageId++,
    role: 'ai',
    content: ''
  }

  messages.value.push(aiMessage)
  isTyping.value = true

  try {
    const reply = await callAI(question)
    for (let i = 0; i < reply.length; i++) {
      aiMessage.content += reply[i]
      await wait(15)
      await scrollChatToBottom()
    }
  } catch (e) {
    aiMessage.content = '❌ AI请求失败'
  }

  isTyping.value = false
  saveHistory()
}

const quickAsk = (text) => {
  input.value = text
  sendMessage()
}

const askToolMore = (tool) => {
  input.value = `介绍一下${tool.name}的使用技巧`
  sendMessage()
}

const askQuizAI = () => {
  input.value = `解释为什么答案是${currentQuiz.value.answer}`
  sendMessage()
}

const askVideoAI = () => {
  input.value = `总结一下${currentTool.value.name}视频重点`
  sendMessage()
}

const wait = (ms) => new Promise(r => setTimeout(r, ms))

const scrollChatToBottom = async () => {
  await nextTick()
  if (chatListRef.value) {
    chatListRef.value.scrollTop = chatListRef.value.scrollHeight
  }
}

const clearChat = () => {
  messages.value = []
  localStorage.removeItem(STORAGE_KEY)
}

const escapeHtml = (text) =>
  text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

const renderMarkdown = (text) => {
  let html = escapeHtml(text)
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\n/g, '<br>')
  return html
}
</script>

<style scoped>
/* ================== 页面统一系统 ================== */

/* 页面整体节奏 */
.learning-page {
  display: flex;
  flex-direction: column;
  gap: 24px;   /* ✅ 核心：统一间距 */
}

/* 每个模块统一容器 */
.page-block {
  margin: 0;   /* ❌ 禁止自己乱加间距 */
}

/* 所有卡片统一风格 */
.learning-page :deep(.content-card) {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.05);

  /* ❗关键：清除组件自己的 margin */
  margin: 0;
}



.learning-page {
  min-height: 100vh;
  padding: 28px 28px 160px;

  /* ✅ 统一背景 */
  background: #f6f9f7;

  overflow-y: auto;
  box-sizing: border-box;
}

@media (max-width: 900px) {
  .learning-page {
    padding: 20px 16px 150px;
  }
}

.learning-page :deep(.content-card) {
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.04);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 20px;
}

.learning-page :deep(.content-card:hover) {
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(101, 131, 103, 0.12);
}

.learning-page :deep(.section-title-row) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.learning-page :deep(.section-title) {
  font-size: 20px;
  font-weight: 700;
  color: #2f3e2f;
}

.learning-page :deep(.section-subtitle) {
  color: #78907b;
  font-size: 13px;
}

.learning-page :deep(.primary-btn),
.learning-page :deep(.ghost-btn),
.learning-page :deep(.clear-btn),
.learning-page :deep(.robot-btn),
.learning-page :deep(.quick-btn),
.learning-page :deep(.send-btn),
.learning-page :deep(.quiz-option) {
  transition: all 0.3s ease-in-out;
}

.learning-page :deep(.primary-btn) {
  background: #4caf50;
  color: #fff;
  border-radius: 10px;
  padding: 10px 16px;
  font-weight: 600;
}

.learning-page :deep(.primary-btn:hover) {
  transform: translateY(-2px);
}

.learning-page :deep(.ghost-btn) {
  border: 1px solid rgba(76, 175, 80, 0.24);
  background: #fff;
  color: #2f7d32;
  padding: 12px 18px;
  border-radius: 14px;
  font-weight: 700;
  cursor: pointer;
}

.learning-page :deep(.ghost-btn:hover) {
  background: #f4fbf4;
  transform: translateY(-2px);
}

.learning-page :deep(.clear-btn) {
  border: none;
  background: rgba(76, 175, 80, 0.12);
  color: #2f7d32;
  border-radius: 12px;
  padding: 10px 14px;
  font-weight: 700;
  cursor: pointer;
}

.learning-page :deep(.clear-btn:hover) {
  transform: translateY(-2px);
}

.learning-page :deep(.fade-slide-enter-active),
.learning-page :deep(.fade-slide-leave-active) {
  transition: all 0.3s ease-in-out;
}

.learning-page :deep(.fade-slide-enter-from),
.learning-page :deep(.fade-slide-leave-to) {
  opacity: 0;
  transform: translateY(12px);
}

.learning-page :deep(.expand-enter-active),
.learning-page :deep(.expand-leave-active) {
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.learning-page :deep(.expand-enter-from),
.learning-page :deep(.expand-leave-to) {
  opacity: 0;
  max-height: 0;
}

.learning-page :deep(.expand-enter-to),
.learning-page :deep(.expand-leave-from) {
  opacity: 1;
  max-height: 220px;
}

.learning-page :deep(.quiz-result) {
  animation: popIn 0.35s ease;
}
  /* ✅ 全局模块间距系统 */
.page-block {
  margin-top: 24px;
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.96);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 1200px) {
  .learning-page :deep(.tool-detail),
  .learning-page :deep(.video-layout) {
    grid-template-columns: 1fr;
  }

  
}

@media (max-width: 900px) {
  .learning-page :deep(.hero-title) {
    font-size: 28px;
  }

  .learning-page :deep(.quiz-options) {
    grid-template-columns: 1fr;
  }

  

  .learning-page {
    padding-bottom: 160px;
  }



}
</style>