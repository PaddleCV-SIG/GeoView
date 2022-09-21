<template>
  <el-row>
    <el-col >
      <el-card  style="margin-bottom: 10px">
        <el-empty
          :image-size="200"
          v-if="this.beforeImg.length == 0"
        ></el-empty>
        <el-row :gutter="10">
          <el-col  :lg="5" :xl="5"
            ><div
              v-for="index in beforeList.length"
              class="img-index hidden-sm-and-down"  :style="{ height:  this.indexHeight + 'rem' }"
            >
              第<span class="index-number">{{ index }}</span
              >组
            </div></el-col
          >
          <el-col :xs="20" :sm="10" :md="6" :lg="6" :xl="6" >
            <div v-for="(item, index) in beforeList" style="position: relative;">
              <el-image
                :src="beforeList[index]"
                :fit="fit"
                :lazy="true"
                ref="tableTab"
                class="gobig"
                :preview-src-list="[beforeList[index]]"
                :preview-teleported="true"
              ></el-image>
         
              <div class="img-infor">
                <span
                  >原图</span
                >
  
              </div>
            </div>
          </el-col>
          <el-col :xs="1" :sm="1" :md="2" :lg="2" :xl="2"></el-col>
          <el-col :xs="20" :sm="10" :md="6" :lg="6" :xl="6" >
            <div v-for="(item, index) in afterList" style="position: relative">
              <el-image
                :src="afterList[index]"
                :fit="fit"
                 :lazy="true"
                ref="tableTab"
                class="gobig"
                :preview-src-list="[afterList[index]]"
                :preview-teleported="true"
           
              ></el-image>
              <div class="img-infor">
                <span
                  >预测结果</span
                >
                <span
                  @click="
                    downloadimgWithWords(
                      index + 1,
                      afterList[index],
                      `${this.funtype}结果图.png`
                    )
                  "
                  ><i class="iconfont icon-xiazai"></i
                ></span>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import { downloadimgWithWords } from "@/utils/download.js";

export default {
  name: "imgshow",
  props: {
    beforeImg: {},
    afterImg: {},
    funtype: "",
  },
  data() {
    return {
      indexHeight:'',
      beforeList: [],
      afterList: [],
      feedBackVisible: false,
      previewPic1: "",
      dialogVisible: false,
      fit: "fill",
      form: {
        content: "",
        type: this.funtype,
        analysis_id: "",
      },
      formLabelWidth: "120px",
      value: null,
      iconClasses: ["icon-rate-face-1", "icon-rate-face-2", "icon-rate-face-3"],
    };
  },
  watch:{
    data() {
      return {
        
      }
    },
  },
  created() {
        if(this.funtype == '地物分类'){
      this.indexHeight = 19
    }
    if(this.funtype == '目标检测'){
      this.indexHeight = 23.4375
    }
  },
  mounted() {
    setTimeout(() => {
      this.beforeList = this.beforeImg.map((item) => {
        return item.before_img;
      });
      this.afterList = this.afterImg.map((item) => {
        return item.after_img;
      });
    }, 500);
  },
  updated() {
    setTimeout(() => {
      this.beforeList = this.beforeImg.map((item) => {
        return item.before_img;
      });
      this.afterList = this.afterImg.map((item) => {
        return item.after_img;
      });
  
    }, 500);
  },
  methods: {
    downloadimgWithWords,
  },
};
</script>

<style scoped lang="less">
* {
  font-family: SimHei sans-serif;
}

.feed-back {
  border: 3px solid #0f2d2d;
  width: 880px;
  margin-bottom: 30px;
  border-radius: 5px;
  font-size: 18px;
  font-family: Microsoft YaHei;
}
.img-index {
  text-align: center;

  align-content: center;
  line-height: 19rem
}
.index-number {
  font-family: Yu Gothic Medium;
  font-style: oblique;
  font-size: 30px;
  margin-left: 5px;
  margin-right: 10px;
}
.img-infor {
  text-align: center;
  font-size: 18px;
  margin-top: 5px;
  margin-bottom: 10px;
  height: 30px;
  font-weight: 500;
  font-family: Microsoft JhengHei UI, sans-serif;
}
.icon-xiazai {
  margin-left: 5px;
  font-size: 24px;
}
.icon-fankui {
  font-size: 24px;
  color: skyblue;
}
</style>