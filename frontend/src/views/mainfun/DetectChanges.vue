<template>
  <div>
    <Tabinfor>
      <template #left>
        <div
          id="sub-title"
        >
          变化检测<i
            class="iconfont icon-dianji"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <p>
      请上传包含<span class="go-bold">图片的文件夹</span><i
        class="iconfont icon-wenjianjia"
      />或者<span
        class="go-bold"
      >图片</span><i
        class="iconfont icon-tupiantianjia"
      />，确保上传的文件夹和图片<span class="go-bold">格式正确</span>，属于一组的图片<span class="go-bold">分别</span>放在两个文件夹里<i
        class="iconfont icon-duigou"
      />
    </p>
    <p style="text-decoration: underline">
      <i
        class="iconfont icon-zhuyi"
      />注意，请将属于<span class="go-bold">同一组</span>的图片设置<span class="go-bold">相同</span>的命名，这将成为我们处理一组图片的依据
    </p>
    <el-card style="border: 4px dashed var(--el-border-color)">
      <div
        v-if="fileList1.length||fileList2.length"
        class="clear-queue"
      >
        <el-button
          type="primary"
          class="btn-animate2 btn-animate__surround"
          @click="clearQueue"
        >
          清空图片
        </el-button>
      </div>
      <el-row
        :gutter="20"
        justify="space-evenly"
      >
        <el-upload
          ref="uploadA"
          v-model:file-list="fileList1"
          drag
          action="#"
          multiple
          :auto-upload="false"
          @change="checkFile1"
        >
          <i class="iconfont icon-yunduanshangchuan" />
          <div class="el-upload__text">
            将文件夹或图片拖到此处，或<em>点击上传</em>
          </div>
          <div
            class="el-upload__tip"
          >
            只能上传一张或多张图片，请在下方上传文件夹
          </div>
        </el-upload>
        <el-upload
          ref="uploadB"
          v-model:file-list="fileList2"
          drag
          action="#"
          multiple
          :auto-upload="false"
          @change="checkFile2"
        >
          <i class="iconfont icon-yunduanshangchuan" />
          <div class="el-upload__text">
            将文件夹或图片拖到此处，或<em>点击上传</em>
          </div>
          <div
            class="el-upload__tip"
          >
            只能上传一张或多张图片，请在下方上传文件夹
          </div>
        </el-upload>
      </el-row>
      <el-row justify="center">
        <el-row class="folder-uploadA">
          <input
            id="upload-fileA"
            ref="refFileA"
            type="file"
            webkitdirectory
            directory
            multiple
            @change="uploadFirst"
          >
          <i
            class="iconfont icon-wenjianshangchuan"
            @click="file1Click"
          >上传文件夹</i>
        </el-row>
        <el-row class="folder-uploadB">
          <input
            id="upload-fileB"
            ref="refFileB"
            type="file"
            webkitdirectory
            directory
            multiple
            @change="uploadSecond"
          >
          <i
            class="iconfont icon-wenjianshangchuan"
            @click="file2Click"
          >上传文件夹</i>
        </el-row>
      </el-row>

      <el-row
        justify="center"
        align="middle"
      >
        <i
          class="iconfont icon-tuxingtuxiangchuli"
        /><p>图像预处理：</p>
        <p>
          <label class="prehandle-label container">
            <input
              ref="histogram"
              type="checkbox"
              @change="selectHistogram()"
            >
            <span class="checkmark" />
            <span class="go-bold label-words">直方图匹配</span>
          </label>

          <label class="container prehandle-label">
            <input
              ref="sharpen"
              type="checkbox"
              @change="selectSharpen()"
            >
            <span class="checkmark" />
            <span class="go-bold label-words">锐化</span>
          </label>
        </p>
      </el-row>
      <el-row
        justify="center"
        align="middle"
      >
        <i
          class="iconfont icon-agora_AIjiangzao"
        /> <p>降噪处理：</p>
        <p>
          <label class="container prehandle-label">
            <input
              ref="smooth"
              type="checkbox"

              @change="selectSmooth()"
            >
            <span class="checkmark " />
            <span class="go-bold label-words">平滑</span>
          </label>
          <label class="container prehandle-label">
            <input
              ref="filter"
              type="checkbox"
              @change="selectFilter()"
            >
            <span class="checkmark " />
            <span class="go-bold label-words">滤波</span>
          </label>
        </p>
      </el-row>

      <el-row
        type="flex"
        justify="center"
      >
        <div class="handle-button">
          <el-button
            type="primary"
            class=" btn-animate btn-animate__shiny"
            @click="uploadfile"
          >
            开始处理
          </el-button>
        </div>
      </el-row>
      <el-divider v-if="!upload.prehandle" />
      <div v-if="upload.prehandle">
        <div v-if="upload.prehandle===1">
          <div
            id="sub-title"
          >
            直方图匹配结果预览
            <i
              class="iconfont icon-dianji"
            />
          </div>
          <el-divider />
          <el-row
            justify="center"
            :gutter="20"
          >
            <el-col
              :xs="24"
              :sm="24"
              :md="7"
              :lg="7"
              :xl="7"
            >
              <div
                v-for="(item,index) in Img1"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  第一时期图
                </div>
              </div>
            </el-col>
            <el-col
              :xs="24"
              :sm="24"
              :md="7"
              :lg="7"
              :xl="7"
            >
              <div
                v-for="(item,index) in Img2"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  匹配后的第一时期图       <span
                    @click="
                      downloadimgWithWords(
                        ++hisNum,
                        item,
                        `直方图匹配后第一时期图.png`
                      )
                    "
                  ><i class="iconfont icon-xiazai" /></span>
                </div>
              </div>
            </el-col>
            <el-col
              :xs="24"
              :sm="24"
              :md="7"
              :lg="7"
              :xl="7"
            >
              <div
                v-for="(item,index) in Img3"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  第二时期图
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
        <div v-else-if="upload.prehandle === 4">
          <div
            id="sub-title"
          >
            锐化结果预览<i
              class="iconfont icon-dianji"
            />
          </div>
          <el-divider />
          <el-row
            justify="center"
            :gutter="20"
          >
            <el-col
              :xs="10"
              :sm="10"
              :md="6"
              :lg="6"
              :xl="6"
            >
              <div
                v-for="(item,index) in Img1"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  第一时期图
                </div>
              </div>
            </el-col>
            <el-col
              :xs="10"
              :sm="10"
              :md="6"
              :lg="6"
              :xl="6"
            >
              <div
                v-for="(item,index) in sharpenImg1"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  锐化后的第一时期图       <span
                    @click="
                      downloadimgWithWords(
                        -1,
                        item,
                        `锐化处理后第一时期图.png`
                      )
                    "
                  ><i class="iconfont icon-xiazai" /></span>
                </div>
              </div>
            </el-col>
            <el-col
              :xs="10"
              :sm="10"
              :md="6"
              :lg="6"
              :xl="6"
            >
              <div
                v-for="(item,index) in Img3"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  第二时期图
                </div>
              </div>
            </el-col>
            <el-col
              :xs="10"
              :sm="10"
              :md="6"
              :lg="6"
              :xl="6"
            >
              <div
                v-for="(item,index) in sharpenImg2"
                :key="index"
              >
                <el-image
                  :src="item"
                  :preview-src-list="[item]"
                  :preview-teleported="true"
                /><div class="handle-words">
                  锐化后的第二时期图       <span
                    @click="
                      downloadimgWithWords(
                        -1,
                        item,
                        `锐化处理后第二时期图.png`
                      )
                    "
                  ><i class="iconfont icon-xiazai" /></span>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-card>

    <Tabinfor>
      <template #left>
        <div
          id="sub-title"
          style="font-size: 25px"
        >
          结果图预览<i
            class="iconfont icon-dianji"
          />
        </div>
      </template>
    </Tabinfor>
    <el-divider />
    <Tabinfor>
      <template #left>
        <p>
          对输出的结果图进行<span class="go-bold">多种渲染</span><i
            class="iconfont icon-xuanran"
          />
          <span class="go-bold">，点击图片</span>即可预览
          <i
            class="iconfont icon-duigou"
          />
        </p>
      </template>
      <template #mid>
        <p v-if="isUpload">
          <label class="prehandle-label container">
            <input
              ref="hole"
              type="checkbox"
              :checked="isHole[currentIndex]"
              @click="dealAfterImg(currentIndex)"
            >
            <span class="checkmark" />
            <span class="go-bold label-words"><span class="hidden-md-and-down">开启连通域滤波并填充</span>孔洞处理</span>
          </label>

          <span><i
            class="iconfont icon-qiehuan"
            @click="changePreMode"
          >切换预览模式</i></span>
        </p>

        <p
          v-else
        >
          <label class="prehandle-label container">
            <input
              ref="hole1"
              type="checkbox"
              :checked="true"
              @click="dealExample()"
            >
            <span class="checkmark" />
            <span class="go-bold label-words">开启连通域滤波并填充孔洞处理</span>
          </label>
          <span><i
            class="iconfont icon-qiehuan"
            @click="changePreMode"
          >切换预览模式</i></span>
        </p>
      </template>
      <template #right>
        <p>
          <span class="go-bold"><i
            class="iconfont icon-shuaxin"
            style="padding-right:33px"
            @click="getMore"
          ><span class="hidden-sm-and-down">点击刷新</span></i></span>
        </p>
      </template>
    </Tabinfor>

    <el-card class="render-box">
      <el-row
        justify="center"
        :gutter="20"
      >
        <el-col
          v-show="preMode===1"
          :xs="12"
          :sm="12"
          :md="12"
          :lg="10"
          :xl="10"
        >
          <p class="handle-words">
            上传第一时期和第二时期图
          </p>
          <div
            v-if="!isUpload"
            id="image-slider"
            @mousemove="sliderMouseMove"
            @mousedown="sliderMouseDown"
            @mouseup="sliderMouseUp"
            @mouseleave="sliderMouseLeave"
          >
            <img
              :src="require('@/assets/image/example/test_50_1.png')"
              alt="预设"
            >
            <div class="img-wrapper">
              <img
                :src="require('@/assets/image/example/test_50_2.png')"
                alt="预设"
              >
            </div>
            <div class="handle">
              <div class="handle-line" />
              <div class="handle-circle">
                &#171;&#187;
              </div>
              <div class="handle-line" />
            </div>
          </div>
          <div
            v-else
            id="image-slider"
            @mousemove="sliderMouseMove"
            @mousedown="sliderMouseDown"
            @mouseup="sliderMouseUp"
            @mouseleave="sliderMouseLeave"
          >
            <img
              :src="beforeImg[currentIndex]"
              alt=""
            >
            <div class="img-wrapper">
              <img
                :src="beforeImg1[currentIndex]"
                alt=""
              >
            </div>
            <div class="handle">
              <div class="handle-line" />
              <div class="handle-circle">
                &#171;&#187;
              </div>
              <div class="handle-line" />
            </div>
          </div>
        </el-col>
        <el-col
          v-show="preMode === 1"
          :xs="12"
          :sm="12"
          :md="12"
          :lg="10"
          :xl="10"
        >
          <div class="render-img">
            <p class="handle-words">
              预测结果
            </p>
            <el-image
              v-if="afterImg.length !== 0"
              :preview-src-list="[showingList[currentIndex]]"
              :preview-teleported="true"
              :src="src"
              fit="cover"
              style="width: 100%"
            />
            <div v-else>
              <el-image
                v-if="renderstyle==='原图'"
                :preview-src-list="[require('@/assets/image/example/normal.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/normal.png')"
                fit="cover"
                style="width: 100%"
              />
              <el-image
                v-else-if="renderstyle==='森林'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/woods.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='霓虹'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/neon.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='闪电'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/flash.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='极光'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/aurora.png')"
                fit="cover"
                style="width: 100%"
              />
            </div>
          </div>
        </el-col>
        <el-col
          v-show="preMode===2"
          :xs="8"
          :sm="8"
          :md="8"
          :lg="6"
          :xl="6"
        >
          <div class="render-img">
            <p class="handle-words">
              第一时期
            </p>
            <el-image
              v-if="afterImg.length !== 0"
              :preview-src-list="[beforeImg[currentIndex]]"
              :preview-teleported="true"
              :src="beforeImg[currentIndex]"
              fit="cover"
              style="width: 100%"
            />
            <el-image
              v-else
              :preview-src-list="[require('@/assets/image/example/test_50_1.png')]"
              :preview-teleported="true"
              :src="require('@/assets/image/example/test_50_1.png')"
              fit="cover"
              style="width: 100%"
            />
          </div>
        </el-col>
        <el-col
          v-show="preMode===2"
          :xs="8"
          :sm="8"
          :md="8"
          :lg="6"
          :xl="6"
        >
          <div class="render-img">
            <p class="handle-words">
              第二时期
            </p>
            <el-image
              v-if="afterImg.length !== 0"
              :preview-src-list="[beforeImg1[currentIndex]]"
              :preview-teleported="true"
              :src="beforeImg1[currentIndex]"
              fit="cover"
              style="width: 100%"
            />
            <el-image
              v-else
              :preview-src-list="[require('@/assets/image/example/test_50_2.png')]"
              :preview-teleported="true"
              :src="require('@/assets/image/example/test_50_2.png')"
              fit="cover"
              style="width: 100%"
            />
          </div>
        </el-col>
        <el-col
          v-show="preMode === 2"
          :xs="8"
          :sm="8"
          :md="8"
          :lg="6"
          :xl="6"
        >
          <div class="render-img">
            <p class="handle-words">
              预测结果
            </p>
            <el-image
              v-if="afterImg.length !== 0"
              :preview-src-list="[showingList[currentIndex]]"
              :preview-teleported="true"
              :src="src"
              fit="cover"
              style="width: 100%"
            />
            <div v-else>
              <el-image
                v-if="renderstyle==='原图'"
                :preview-src-list="[require('@/assets/image/example/normal.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/normal.png')"
                fit="cover"
                style="width: 100%"
              />
              <el-image
                v-else-if="renderstyle==='森林'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/woods.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='霓虹'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/neon.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='闪电'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/flash.png')"
                fit="cover"
                style="width: 100%"
              />    <el-image
                v-else-if="renderstyle==='极光'"
                :preview-src-list="[require('@/assets/image/example/aurora.png')]"
                :preview-teleported="true"
                :src="require('@/assets/image/example/aurora.png')"
                fit="cover"
                style="width: 100%"
              />
            </div>
          </div>
        </el-col>
        <el-col
          :xs="24"
          :sm="24"
          :md="24"
          :lg="4"
          :xl="4"
        >
          <div class="rendr-style">
            <el-divider />
            <div class="style-title">
              结果图渲染
            </div>

            <label class="cl-checkbox">
              <el-row justify="center">
                <el-col><div
                          class="style-words normal"
                          :class="{ 'active-normal': renderstyle === '原图' }"
                          @click="setNormalWay(onRender)"
                        >原图</div>
                  <div
                    class="style-words woods"
                    :class="{ 'active-woods': renderstyle === '森林' }"
                    @click="setWoods(onRender)"
                  >森林</div>
                  <div
                    class="style-words neon"
                    :class="{ 'active-neon': renderstyle === '霓虹' }"
                    @click="setneon(onRender)"
                  >霓虹</div>
                  <div
                    class="style-words flash"
                    :class="{ 'active-flash': renderstyle === '闪电' }"
                    @click="setFlash(onRender)"
                  >闪电</div>
                  <div
                    class="style-words aurora"
                    :class="{ 'active-aurora': renderstyle === '极光' }"
                    @click="setAurora(onRender)"
                  >极光</div></el-col>
              </el-row>
            </label>
          </div>
          <el-divider style="margin-top:0" />
          <div class="style-title">
            选择图片
          </div>

          <el-empty
            v-if="showingList.length === 0"
            :image-size="100"
          />
          <div
            v-for="(item, index) in Math.ceil(showingList.length / 5)"
            :key="index"
            class="list"
          >
            <div
              class="list-number"
              @click="goRenderThese(index)"
            >
              <div>
                {{ 5 * index + 1 }}-----{{ 5 * (index + 1) }}
              </div>
            </div>
          </div>
          <div
            v-if="isUpload"
            style="text-align:center"
          >
            下载此图片：<el-button
              type="primary"
              style="width:60px"
              class="btn-animate btn-animate__shiny"
              @click="
                downloadimgWithWords(
                  idList[currentIndex],
                  showingList[currentIndex],
                  `变化检测${renderstyle}渲染结果图.png`
                )
              "
            >
              下载
            </el-button>
          </div>
          <p
            v-if="isUpload"
            style="text-align:center"
          >
            <span> <i
              class="iconfont icon-dabaoxiazai"
              @click="goCompress"
            >所有结果图打包</i></span>
          </p>
        </el-col>
      </el-row>
      <el-row class="swiper-img">
        <div
          v-for="(item, index) in 5"
          :key="index"
          class="img-box"
        >
          <el-image
            v-if="isExist[index]"
            :src="srcs[index]"
            :class="{'render-border':onRender===index}"
            @click="goRenderThis(index)"
          />
        </div>
      </el-row>
    </el-card>
    <Bottominfor />
  </div>
</template>


<script>
import { showFullScreenLoading, hideFullScreenLoading } from "@/utils/loading";
import {
  createSrc,
  detectChangesUpload,
  holeHandle,
  histogramUpload,
} from "@/api/upload";
import {
  downloadimgWithWords,
  getImgArrayBuffer,
  atchDownload,
} from "@/utils/download.js";
import { historyGetPage } from "@/api/history";
import Tabinfor from "@/components/Tabinfor";
import Bottominfor from "@/components/Bottominfor";
import global from "@/global";
export default {
  name: "Detectchanges",
  components: {
    Tabinfor,
    Bottominfor,
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      document.querySelector(".el-main").scrollTop = 0;
    });
  },
  data() {
    return {
      isSliderLocked: false,
      preMode: 1,
      pairs: [],
      hisPairs: [],
      shaPairs: [],
      canUpload: true,
      onRender: 0,
      onRenderGroup: 0,
      isHole: [],
      isUpload: true,
      idIndex: 0,
      isExist: [],
      downnumber: 0,
      hisNum: 0,
      value:null,
      renderstyle: "原图",
      funtype: "变化检测",
      scrollTop: "",
      afterImg: [],
      afterList: [],
      woods: [],
      neon: [],
      flash: [],
      aurora: [],

      showingList: [],
      beforeImg: [],
      beforeImg1: [],
      currentQroup: 0,
      src:'',
      srcs: [
      ],
      example: {
        outcome: [
        ],
        first: [
        ],
        second: [],
        normal: [
        ],
        woods: [
        ],
        neon: [
        ],
        flash: [
        ],
        aurora: [
        ],
      },
      currentIndex: 0,
      fileList1: [],
      fileList2: [],

      uploadSrc1: [],
      uploadSrc2: [],
      uploadSrc: [],
      upload: {
        list: [
          {
            first: "",
            second: "",
          },
        ],
        prehandle: 0,
        denoise: 0,
      },

      //直方图处理
      uploadSrc3: [],
      uploadSrc4: [],
      histogramSrc: [],
      myhistogram: {
        list: [
          {
            first: "",
            second: "",
          },
        ],
        prehandle: 0,
      },
      Img1: [],
      Img2: [],
      Img3: [],

      //锐化处理
      sharpenSrc1: [],
      sharpenSrc2: [],
      sharpenSrc: [],
      mysharpen: {
        list: [
          {
            first: "",
            second: "",
          },
        ],
        prehandle: 0,
      },
      sharpenImg1: [],
      sharpenImg2: [],

      preHandle: {
        list: [
          {
            first: "",
            second: "",
          },
        ],
      },

      idList: [],
      hole: {
        id: "",
      },

    };
  },
  created() {
    this.getMore();
  },

  methods: {
    downloadimgWithWords,
    historyGetPage,
    detectChangesUpload,
    createSrc,
    getImgArrayBuffer,
    atchDownload,
    holeHandle,
    histogramUpload,
    clearQueue() {
      this.fileList1 = [];
      this.fileList2 = [];
      this.$message.success("清除成功");
    },
    checkUpload() {
      if (this.afterImg.length === 0) {
        this.isUpload = false;
      }
    },
    checkExist(val) {
      this.isExist = val.map((item) => {
        return typeof item != "undefined";
      });
    },
    goRenderThis(index) {
      this.currentIndex = this.currentQroup;
      this.currentIndex += index;
      if (this.showingList.length !== 0) {
        this.src = this.showingList[this.currentIndex];
      } else {
        this.src = this.srcs[index];
      }
      this.onRender = index;
    },
    goRenderThese(index) {

      this.onRenderGroup = index;

      this.currentQroup = 5 * index;
      this.currentIndex = 5 * index;
      this.srcs = [];

      for (let i = 0; i <= 4; i++) {
        this.srcs.push(this.showingList[this.currentIndex++]);
      }
      this.src = this.srcs[0];
      this.idIndex = this.currentIndex;
      this.goRenderThis(0);
      this.checkExist(this.srcs);
    },

    setNormalWay(render) {
      this.renderstyle = "原图";
      this.showingList.splice(0, this.showingList.length);
      if (this.isUpload === false) {
        this.showingList.push(this.example.normal[0]);
      } else {
        this.showingList.push(...this.afterList);
      }
      this.goRenderThese(this.onRenderGroup);
      this.goRenderThis(render);
    },
    setWoods(render) {
      this.renderstyle = "森林";
      this.showingList.splice(0, this.showingList.length);
      if (this.isUpload === false) {
        this.showingList.push(this.example.woods[0]);
      } else {
        this.showingList.push(...this.woods);
      }
      this.goRenderThese(this.onRenderGroup);
      this.goRenderThis(render);
    },
    setneon(render) {
      this.renderstyle = "霓虹";

      this.showingList.splice(0, this.showingList.length);
      if (this.isUpload === false) {
        this.showingList.push(this.example.neon[0]);
      } else {
        this.showingList.push(...this.neon);
      }
      this.goRenderThese(this.onRenderGroup);
      this.goRenderThis(render);
    },
    setFlash(render) {
      this.renderstyle = "闪电";

      this.showingList.splice(0, this.showingList.length);
      if (this.isUpload === false) {
        this.showingList.push(this.example.flash[0]);
      } else {
        this.showingList.push(...this.flash);
      }

      this.goRenderThese(this.onRenderGroup);
      this.goRenderThis(render);
    },
    setAurora(render) {
      this.renderstyle = "极光";
      this.showingList.splice(0, this.showingList.length);
      if (this.isUpload === false) {
        this.showingList.push(this.example.aurora[0]);
      } else {
        this.showingList.push(...this.aurora);
      }
      this.goRenderThese(this.onRenderGroup);
      this.goRenderThis(render);
    },
    uploadfile() {
      this.uploadSrc = [];
      if (
          this.fileList1.length !== this.fileList2.length ||
          this.fileList1.length === 0
      ) {
        this.$message.error("请按照要求上传文件夹或图片！");
      } else {
        showFullScreenLoading("#load");
        let formData1 = new FormData();
        let formData2 = new FormData();
        for (const item of this.fileList1) {
          formData1.append("files", item) ||
          formData1.append("files", item.raw);
          formData1.append("type", "变化检测");
        }
        for (const item of this.fileList2) {
          formData2.append("files", item) ||
          formData2.append("files", item.raw);
          formData2.append("type", "变化检测");
        }
        let upload1 = new Promise((resolve, reject) => {
          setTimeout(() => {
            this.createSrc(formData1).then((res) => {
              this.uploadSrc1 = res.data.data;
              resolve();
            });
          }, 200);
        });
        let upload2 = new Promise((resolve, reject) => {
          this.createSrc(formData2).then((res) => {
            this.uploadSrc2 = res.data.data;
            resolve();
          });
        });
        Promise.all([upload1, upload2])
            .then((val) => {
              this.uploadSrc = this.uploadSrc1.concat(this.uploadSrc2);
              this.uploadSrc = this.uploadSrc.map((item) => {
                return {
                  filename: item.filename.substring(
                      item.filename.indexOf("/") + 1,
                      item.length
                  ),
                  src: item.src,
                };
              });

              this.pairs = this.uploadSrc.map((item) => {
                return item.filename.substring(
                    item.filename.indexOf("/") + 1,
                    item.length
                );
              });

              this.checkPairs(this.pairs);
              if (!this.canUpload) {
                this.$message.error(
                    "检测到命名对应失败的图片，请检查您的文件命名"
                );
                hideFullScreenLoading("#load");
              } else {
                this.getList(this.uploadSrc);
                this.detectChangesUpload(this.upload)
                    .then((res) => {
                      if (res.data.code === 1) {
                        this.$message.error(res.data.msg);
                      }

                      this.$refs.uploadA.clearFiles();
                      this.$refs.uploadB.clearFiles();
                      this.fileList1 = [];
                      this.fileList2 = [];
                      this.$message.success("上传成功");
                      this.isUpload = true;
                      this.getMore();
                      hideFullScreenLoading("#load");
                      if (this.afterImg.length >= 20) {
                        this.$confirm(
                            "上传图片过多，是否压缩?",
                            "提示",
                            {
                              confirmButtonText: "确定",
                              cancelButtonText: "取消",
                              type: "warning",
                            }
                        )
                            .then(() => {
                              this.goCompress();
                            })
                            .catch(() => {});
                      }
                    })
                    .catch((rej) => {
                      hideFullScreenLoading("#load");
                    });
              }
            })
            .catch((rej) => {
              hideFullScreenLoading("#load");
            });
      }
    },
    getList(beforeData) {
      //算法参考
      //https://blog.csdn.net/weixin_45575273/article/details/108321137?utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~aggregatepage~first_rank_ecpm_v1~rank_v31_ecpm-3-108321137-null-null.pc_agg_new_rank&utm_term=%E6%95%B0%E7%BB%84%E4%B8%AD%E7%9A%84%E5%AF%B9%E8%B1%A1id%E7%9B%B8%E5%90%8C%E7%9A%84%E5%AF%B9%E8%B1%A1%E7%BB%84%E6%88%90%E4%B8%80%E4%B8%AA%E6%96%B0%E6%95%B0%E7%BB%84&spm=1000.2123.3001.4430
      let tempArr = [];
      let afterData = [];
      for (let i = 0; i < beforeData.length; i++) {
        if (tempArr.indexOf(beforeData[i].filename) === -1) {
          afterData.push(beforeData[i]);
          tempArr.push(beforeData[i].filename);
        } else {
          for (let j = 0; j < afterData.length; j++) {
            Reflect.deleteProperty(afterData[j], "photo_id");
            // Reflect.deleteProperty(afterData[j], "filename");
            afterData[j].first = afterData[j].src;
            afterData[j].second = beforeData[i + j].src;
            // Reflect.deleteProperty(afterData[j], "src");
          }
          break;
        }
      }

      this.upload.list = afterData;
    },
    goCompress() {
      this.$message.success("正在将所有图片下载压缩");
      this.historyGetPage(1, 9999, "变化检测").then((res) => {
        this.atchDownload(
            res.data.data.map((item) => {
              return { after_img: item.after_img, id: item.id };
            })
        );
      });
    },
    getMore() {
      showFullScreenLoading("body");
      this.historyGetPage(1, 20, "变化检测")
          .then((res) => {
            hideFullScreenLoading("body");
            this.beforeImg = res.data.data.map((item) => {
              return global.BASEURL + item.before_img;
            });
            this.idList = res.data.data.map((item) => {
              return item.id;
            });
            this.isHole = res.data.data.map((item) => {
              return item.is_hole;
            });
            this.afterImg = res.data.data.map((item) => {
              return {
                after_img: global.BASEURL + item.after_img,
                id: item.id,
              };
            });

            this.afterList = res.data.data.map((item) => {
              return global.BASEURL + item.after_img;
            });
            this.showingList = res.data.data.map((item) => {
              return global.BASEURL + item.after_img;
            });

            if (this.afterList.length !== 0) {
              this.goRenderThese(0);
              this.goRenderThis(0);
            }
            this.beforeImg1 = res.data.data.map((item) => {
              return global.BASEURL + item.before_img1;
            });
            this.woods = res.data.data.map((item) => {
              return global.BASEURL + item.data[2];
            });
            this.neon = res.data.data.map((item) => {
              return global.BASEURL + item.data[3];
            });
            this.flash = res.data.data.map((item) => {
              return global.BASEURL + item.data[0];
            });
            this.aurora = res.data.data.map((item) => {
              return global.BASEURL + item.data[1];
            });
            this.checkUpload();
            if (!this.isUpload) {
              this.setNormalWay(this.onRender);
            }
          })
          .catch((rej) => {
            hideFullScreenLoading("body");
          });
    },
    uploadFirst() {
      this.checkFile1(...this.$refs.refFileA.files);
      if (this.canUpload) {
        this.fileList1.push(...this.$refs.refFileA.files);
      } else {
        setTimeout(() => {
          this.$message.error("检测到您上传的文件夹内存在不符合规范的图片类型");
        }, 1000);
      }
    },
    uploadSecond() {
      this.checkFile2(...this.$refs.refFileB.files);
      if (this.canUpload) {
        this.fileList2.push(...this.$refs.refFileB.files);
      } else {
        setTimeout(() => {
          this.$message.error("检测到您上传的文件夹内存在不符合规范的图片类型");
        }, 1000);
      }
    },
    file1Click() {
      document.querySelector("#upload-fileA").click();
    },
    file2Click() {
      document.querySelector("#upload-fileB").click();
    },
    selectHistogram() {
      if (this.$refs.histogram.checked === true) {
        if (
            this.fileList1.length !== this.fileList2.length ||
            this.fileList1.length === 0
        ) {
          if (this.upload.prehandle === 1) {
            this.$refs.histogram.checked = false;
            this.upload.prehandle = 0;
          } else {
            this.$refs.histogram.checked = false;
            this.$message.error("请先按要求上传图片");
          }
        } else {
          this.upload.prehandle = 1;
          this.myhistogram.prehandle = 1;
          this.$message.success("直方图处理");
          if (this.$refs.sharpen.checked === true) {
            this.$refs.sharpen.checked = false;
          }
          let formData1 = new FormData();
          let formData2 = new FormData();

          for (const item of this.fileList1) {
            formData1.append("files", item) ||
            formData1.append("files", item.raw);
            formData1.append("type", "变化检测");
          }

          for (const item of this.fileList2) {
            formData2.append("files", item) ||
            formData2.append("files", item.raw);
            formData2.append("type", "变化检测");
          }
          let upload3 = new Promise((resolve, reject) => {
            this.createSrc(formData1).then((res) => {
              this.uploadSrc3 = res.data.data.splice(0, 3);
              this.Img1 = this.uploadSrc3.map((item) => {
                return global.BASEURL + item.src;
              });
              resolve();
            });
          });
          let upload4 = new Promise((resolve, reject) => {
            this.createSrc(formData2).then((res) => {
              this.uploadSrc4 = res.data.data.splice(0, 3);
              this.Img3 = this.uploadSrc4.map((item) => {
                return global.BASEURL + item.src;
              });
              resolve();
            });
          });
          Promise.all([upload3, upload4]).then((val) => {
            this.histogramSrc = this.uploadSrc3.concat(this.uploadSrc4);
            //https://blog.csdn.net/qq_27342239/article/details/118078113去除“/”前的字符
            this.histogramSrc = this.histogramSrc.map((item) => {
              return {
                filename: item.filename.substring(
                    item.filename.indexOf("/") + 1,
                    item.length
                ),
                src: item.src,
              };
            });

            this.hisPairs = this.histogramSrc.map((item) => {
              return item.filename.substring(
                  item.filename.indexOf("/") + 1,
                  item.length
              );
            });

            this.checkPairs(this.hisPairs);

            if (!this.canUpload) {
              this.$message.error(
                  "检测到命名对应失败的图片，请检查您的文件命名"
              );
              hideFullScreenLoading("#load");
              this.Img1 = [];
              this.Img3 = [];
            } else {
              this.createHandelList(this.histogramSrc);
              this.histogramUpload(this.myhistogram).then((res) => {
                this.Img2 = res.data.data.map((item) => {
                  return global.BASEURL + item;
                });
                this.Img2 = this.Img2.splice(0, 3);
              });
            }
          });
        }
      } else {
        this.$message.success("取消直方图处理");
        this.upload.prehandle = 0;
        this.myhistogram.prehandle = 0;
      }
    },
    createHandelList(beforeData) {
      let tempArr = [];
      let afterData = [];
      for (let i = 0; i < beforeData.length; i++) {
        if (tempArr.indexOf(beforeData[i].filename) === -1) {
          afterData.push(beforeData[i]);
          tempArr.push(beforeData[i].filename);
        } else {
          for (let j = 0; j < afterData.length; j++) {
            Reflect.deleteProperty(afterData[j], "photo_id");
            // Reflect.deleteProperty(afterData[j], "filename");
            afterData[j].first = afterData[j].src;
            afterData[j].second = beforeData[i + j].src;
            // Reflect.deleteProperty(afterData[j], "src");
          }
          break;
        }
      }
      this.myhistogram.list = afterData;
    },
    selectSharpen() {
      if (
          this.fileList1.length !== this.fileList2.length ||
          this.fileList1.length === 0
      ) {
        if (this.upload.prehandle === 4) {
          this.$refs.sharpen.checked = false;
          this.upload.prehandle = 0;
        } else {
          this.$refs.sharpen.checked = false;
          this.$message.error("请先按要求上传图片");
        }
      } else {
        if (this.$refs.histogram.checked === true) {
          this.$refs.histogram.checked = false;
        }

        if (this.$refs.sharpen.checked === false) {
          this.myhistogram.prehandle = 0;
          this.$message.success("取消锐化处理");
          this.upload.prehandle = 0;
        } else {
          this.$message.success("锐化处理");
          this.upload.prehandle = 4;
          this.mysharpen.prehandle = 4;
          let formData1 = new FormData();
          let formData2 = new FormData();

          for (const item of this.fileList1) {
            formData1.append("files", item) ||
            formData1.append("files", item.raw);
            formData1.append("type", "变化检测");
          }

          for (const item of this.fileList2) {
            formData2.append("files", item) ||
            formData2.append("files", item.raw);
            formData2.append("type", "变化检测");
          }
          let upload1 = new Promise((resolve, reject) => {
            this.createSrc(formData1).then((res) => {
              this.sharpenSrc1 = res.data.data.splice(0, 3);
              this.Img1 = this.sharpenSrc1.map((item) => {
                return global.BASEURL + item.src;
              });
              resolve();
            });
          });
          let upload2 = new Promise((resolve, reject) => {
            this.createSrc(formData2).then((res) => {
              this.sharpenSrc2 = res.data.data.splice(0, 3);
              this.Img3 = this.sharpenSrc2.map((item) => {
                return global.BASEURL + item.src;
              });
              resolve();
            });
          });
          Promise.all([upload1, upload2]).then((val) => {
            this.sharpenSrc = this.sharpenSrc1.concat(this.sharpenSrc2);
            this.sharpenSrc = this.sharpenSrc.map((item) => {
              return {
                filename: item.filename.substring(
                    item.filename.indexOf("/") + 1,
                    item.length
                ),
                src: item.src,
              };
            });
            this.shaPairs = this.sharpenSrc.map((item) => {
              return item.filename.substring(
                  item.filename.indexOf("/") + 1,
                  item.length
              );
            });

            this.checkPairs(this.hisPairs);

            if (!this.canUpload) {
              this.$message.error(
                  "检测到命名对应失败的图片，请检查您的文件命名"
              );
              hideFullScreenLoading("#load");
              this.Img1 = [];
              this.Img3 = [];
            } else {
              this.createSharpenList(this.sharpenSrc);
              this.histogramUpload(this.mysharpen).then((res) => {
                this.sharpenImg1 = res.data.data.map((item) => {
                  return global.BASEURL + item.first;
                });

                this.sharpenImg2 = res.data.data.map((item) => {
                  return global.BASEURL + item.second;
                });
              });
            }
          });
        }
      }
    },
    createSharpenList(beforeData) {
      let tempArr = [];
      let afterData = [];
      for (let i = 0; i < beforeData.length; i++) {
        if (tempArr.indexOf(beforeData[i].filename) === -1) {
          afterData.push(beforeData[i]);
          tempArr.push(beforeData[i].filename);
        } else {
          for (let j = 0; j < afterData.length; j++) {
            Reflect.deleteProperty(afterData[j], "photo_id");
            // Reflect.deleteProperty(afterData[j], "filename");
            afterData[j].first = afterData[j].src;
            afterData[j].second = beforeData[i + j].src;
            // Reflect.deleteProperty(afterData[j], "src");
          }
          break;
        }
      }
      this.mysharpen.list = afterData;
    },
    selectFilter() {
      if (this.$refs.smooth.checked === true) {
        this.$refs.smooth.checked = false;
      }

      if (this.$refs.filter.checked === false) {
        this.$message.success("取消高斯滤波处理");
        this.upload.denoise = 0;
      } else {
        this.$message.success("高斯滤波处理");
        this.upload.denoise = 5;
      }
    },
    selectSmooth() {
      if (this.$refs.filter.checked === true) {
        this.$refs.filter.checked = false;
      }

      if (this.$refs.smooth.checked === false) {
        this.$message.success("取消平滑处理");
        this.upload.denoise = 0;
      } else {
        this.$message.success("平滑处理");
        this.upload.denoise = 3;
      }
    },
    dealAfterImg(currentIndex) {
      if (this.isHole[currentIndex]) {
        this.$refs.hole.checked = true;
        this.$message.success("该图已经过处理");
      } else {
        this.$message.success("连通域滤波并填充孔洞处理");
        this.hole.id = this.idList[this.currentIndex];
        this.holeHandle(this.hole).then((res) => {
          this.getMore();
        });
      }
    },
    dealExample() {
      this.$refs.hole1.checked = true;
      this.$message.success("该图已经过处理");
    },
    checkFile1(file) {
      const whiteList = ["jpg", "jpeg", "png", "JPG", "JPEG"];

      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error("上传只能是 jpg,jpeg,png,JPG,JPEG格式,请重新上传");
        this.fileList1 = [];
        this.canUpload = false;
      } else {
        this.canUpload = true;
      }
    },
    checkFile2(file) {
      const whiteList = ["jpg", "jpeg", "png", "JPG", "JPEG"];
      const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (whiteList.indexOf(fileSuffix) === -1) {
        this.$message.error("上传只能是 jpg,jpeg,png,JPG,JPEG格式,请重新上传");
        this.fileList2 = [];
        this.canUpload = false;
      } else {
        this.canUpload = true;
      }
    },
    checkPairs(list) {
      let s = list.join(",") + ",";
      let j = 0;
      for (let i = 0; i < list.length; i++) {
        if (s.replace(list[i] + ",", "").indexOf(list[i] + ",") > -1) {
        } else {
          j++;
          break;
        }
      }
      this.canUpload = j === 0;
    },
    changePreMode() {
      if (this.preMode === 1) {
        this.preMode = 2;
      } else {
        this.preMode = 1;
      }
    },
    sliderMouseMove(event) {
      const slider = document.querySelector("#image-slider");
      const wrapper = document.querySelector(".img-wrapper");
      const handle = document.querySelector(".handle");

      if (this.isSliderLocked) return;

      const sliderLeftX = slider.offsetLeft;

      const sliderWidth = slider.clientWidth;

      const sliderHandleWidth = handle.clientWidth;

      let mouseX = event.clientX - sliderLeftX;

      if (mouseX < 0) mouseX = 0;
      else if (mouseX > sliderWidth) mouseX = sliderWidth;

      wrapper.style.width = `${((1 - mouseX / sliderWidth) * 100).toFixed(4)}%`;

      handle.style.left = `calc(${((mouseX / sliderWidth) * 100).toFixed(
          4
      )}% - ${sliderHandleWidth / 2}px)`;

    },
    sliderMouseDown() {
      if (this.isSliderLocked) this.isSliderLocked = false;
      this.sliderMouseMove(event);
    },
    sliderMouseUp() {
      if (!this.isSliderLocked) this.isSliderLocked = true;
    },
    sliderMouseLeave() {
      if (this.isSliderLocked) this.isSliderLocked = true;
    },
  },
};
</script>

<style scoped lang="less">
* {
  font-family: SimHei sans-serif;
}
.list {
  text-align: center;
  cursor: pointer;
  width: auto;
  height: 20px;
  background-color: rgb(236, 244, 255);
  position: relative;
  margin-bottom: 10px;
}
.list-number:hover::after {
  width: 100%;
  background: var(--theme--color);
}
.list-number::after {
  position: absolute;
  content: "";
  width: 0;
  height: 100%;
  top: 0;
  left: 0;
  border-radius: 2px 2px 0 0;
  transition: 0.4s;
  z-index: -1;
}
.list:hover * {
  color: #ecf4ff !important;
}
.list-number {
  z-index: 1;
  overflow: hidden;
  margin: 0 auto;
  width: auto;
  height: 20px;
  position: relative !important;
  border-radius: 2px !important;
}
.swiper-img {
  width: 100%;
  margin-top: 30px;
  overflow: hidden;
  position: relative;
  max-height: 280px;
  min-height: 240px;
  .img-box {
    flex: 1;
    height: 100%;
    overflow: hidden;
    opacity: 0.7;
    transition: all 0.6s;
    margin-right: 10px;
    justify-content: space-between;
  }
}
#sub-title{
  font-size: 25px;
}
#sub-title:hover:after {
  left: 0;
  right: 0;
  width: 220px;
}
.render-box {
  .render-img {
    // width: 100%;
    max-height: 600px;
    overflow: hidden;

  }
  .render-style {
    height: auto;
  }
}
.cl-checkbox {
  display: block;
  height: auto;
  text-align: center;
}

.style-title {
  text-align: center;
  font-size: 22px;
  font-family: "幼圆", sans-serif;
  font-weight: 600;
  margin-bottom: 20px;
}
.img-index {
  text-align: center;
  height: 428px;
  align-content: center;
  line-height: 428px;
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
}
.clear-queue {
  position: absolute;
  left: 0;
  top: 10%;
  z-index: 100;
}
.render-border {
  border: var(--theme--color) 0.5rem solid;
}

#image-slider {
  position: relative;
  max-width:100%;
  max-height: 100%;
  overflow: hidden;
  border-radius: 1em;
  cursor: col-resize;
  display: inline-block;
}

#image-slider img {
  display: block;
  height: 100%;
  max-width:550px;
  max-height: 550px;
  object-fit: cover;
  pointer-events: none;
  user-select: none;
}

#image-slider .img-wrapper {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: 50%;
  overflow: hidden;
  z-index: 1;
}

#image-slider .img-wrapper img {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
}

#image-slider .handle {
  border: 0 solid red;
  position: absolute;
  top: 0;
  left: calc(50% - var(--image-slider-handle-width) / 2);
  width: var(--image-slider-handle-width);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  user-select: none;
  z-index: 2;
}

#image-slider .handle-circle {
  color: white;
  border: 2px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
}

#image-slider .handle-line {
  width: 2px;
  flex-grow: 1;
  background: white;
}

@media (max-width: 768px) {
  :root {
    --image-slider-width: 90vw;
  }
}
.el-row{
  position: inherit;
}
.style-words {
  line-height: 30px;
  height: 30px;
  transition: all 0.4s;
  margin-bottom: 10px;
  cursor: pointer;
  font-size: 18px;
}
.style-words:hover {
  color: white;
}
.normal:hover {
  background-color: var(--theme--color);
}
.woods:hover {
  background-image: linear-gradient(#9be15d, #00e3ae 100%);
}
.neon:hover {
  background-image: linear-gradient(135deg, #f761a1 15%, #8c1bab 100%);
}
.flash:hover {
  background-image: linear-gradient(135deg, #c2ffd8 10%, #465efb 100%);
}
.aurora:hover {
  background-image: linear-gradient(#011142, #00bbc9 100%);
}
.active-normal {
  background-color: rgb(64, 158, 255);
}
.active-woods {
  background-image: linear-gradient(#9be15d, #00e3ae 100%);
}
.active-neon {
  background-image: linear-gradient(135deg, #f761a1 15%, #8c1bab 100%);
}
.active-flash {
  background-image: linear-gradient(135deg, #c2ffd8 10%, #465efb 100%);
}
.active-aurora {
  background-image: linear-gradient(#011142, #00bbc9 100%);
}
</style>