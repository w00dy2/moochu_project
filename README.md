

<div align=center><img src="https://capsule-render.vercel.app/api?type=rounded&color=auto&height=150&section=header&text=MOOCHU&fontSize=90" /></div>

## MOOCHU PROJECT

    `MOOCHU` 는 OTT, 영화관의 영화들의 데이터들을 한 곳에서
    저장된 영화를 기반으로 사용자마다 좋아하는 영화, TV show를 추천 받을 수 있는
    `영화 추천 시스템 웹 서비스` 입니다.

<br>

<details>
<summary>🎤 MOOCHU 바로가기</summary>
<div markdown="1">

<br>
<a href="http://34.64.147.118:8000/moochu" target="_blank" rel="noopener noreferrer">👉🏻Click👈🏻</a>
<br>
</div>
</details>

<br>

## 🧑‍🤝‍🧑 제작 기간 & 참여 인원

  	-  제작 기간 : 2023.06.12 ~ 2023.08.11 (약 2개월)
	-  참여 인원 : 6명
<br>

## ⚙️ 사용 기술 스택

<br>

| ⚙️ 기술 스택 | 👇🏻 사용 목적 |
|--|--|
| **`django`** | MOOCHU 웹 서비스 구현 |
| **`fastapi`** | 추천 모델 serving |
| **`Google Cloud Storage`** | Data Warehouse, 이미지 적재 |
| **`Google BigQuery`** | Data Warehouse, 학습된 모델 파일 적재 |
| **`airflow`** | CGV, Lotte, MegaBox, OTT 개봉예정작 데이터 자동화|
| **`Kafka`** , **`redis`** | 트래픽 분산, 로그 적재 |
| **`Mysql`**, **`mongoDB`** | 데이터베이스 활용 |
| **`nginx`**, **`gunicorn`** | Web서버와 WAS 분리 |
| **`GCP(Google Cloud Platform)`** | 배포를 위한 클라우드 서비스 활용 |
| **`docker`**, **`docker compose`** | 배포를 위한 작업 환경 도커라이징 |
| **`elastic search`**, **`logstash`**, **`kibana`** | 검색 기능 고도화, 데이터 시각화 |

<br>

## ERD 설계
	
![DB ERD](https://github.com/jsjang96/images/blob/master/MOOCHU_erd.png)

<br>

## 핵심 기능
- 이 서비스의 핵심 기능은 **추천 서비스 기능**입니다. <br>
- 사용자가 즐겨서 보는 영화 장르, 영화 리스트를 기반으로 새로운 영화를 추천해주는 서비스입니다. <br>
- 또한, 영화들을 사용자들끼리 추천을 해주고 미니홈피를 만들어 소통도 할 수 있도록 했습니다. <br>
- 그리고, 장르와 OTT별로 본인이 좋아하는 영화들을 필터링하여 볼 수 있습니다.<br>
아래는 **전체 아키텍처**에 대한 첨부파일입니다.

<details>
<summary><b>전체 아키텍처 펼치기</b></summary>
<div align="center" markdown="1">
	<img src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%981.png"/>
	<img src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%982.png"/>
	<img
src="https://github.com/jsjang96/images/blob/master/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%983.png"/>
</div>
</details>
<br>

## 트러블 슈팅

### 1. 크롤링
    - 1.1 셀레니움을 이용하여 직접 OTT 사이트를 크롤링할 경우 지속적인 서비스 유지에 있어 airflow 배치가 불가능하다는 문제가 발생
    - 방안 : 데이터를 가져오는 방식을 바꿔 추가로 가져오는 데이터는 netflix, watcha, megawbox, CGV로 수정

    - 1.2 크롤링을 통해 메인 db를 구축하는 과정에 있어서 일정 데이터 개수가 넘어가면 IP blocking이 발생
<br>

####  팀원들과 분산작업 (에러 해결)
#### <img src="https://github.com/jsjang96/images/blob/master/%ED%8C%80%EC%9B%90%20%EB%B6%84%EC%82%B0%20%ED%81%AC%EB%A1%A4%EB%A7%81%20-%20%EB%AC%B8%EC%A0%9C%ED%95%B4%EA%B2%B0.png"/>
<br>

### 2. Airflow - mongodb - googlestorage
    2.1 각각의 덱을 짜서 작업을 실행했을경우 같은 영화 정보를 처리하기 위해 read write를 계속 반복해야하는 문제가 있었음.
    - 하나의 덱으로 만들어 중복 데이터를 처리할 수 있게 작성
  
    2.2 실제서비스를 고려하여 googlestorage에 포스터를 적재하는 흐름을 추가
      - 해당 작업에서 고유한 id를 이용하기 위해 mongodb에서 자동 생성한 고유필드인 _id를 기준으로 storage에 적재하기로 결정
      - 먼저 _id값을 어떻게 다음 task에 넘겨줄 것인지에 고민
      -> xcom을 이용하여 mongodb에 적재되는 과정에서 알 수 있는 _id값과 href 값을 넘겨주기로 결정 (limit 48kb)
      - 각각의 task에서 push한 xcom을 merge하는 task를 거쳐 googlestorage 적재 task를 실행


### 3. Elasticsearch - mongoDB 연동 실패
    - mysql, PostgreSQL - Elasticsearch 연동은 잘 됐음. ( 관계형 DB와 elasticserach의 연동은 문제 없음 )
    - Mongodb(Nosql) - Elasticsearch 연동 실패
<br>

### 4. Cloud에 띄워져 있는 mongoDB 해킹
    - Cloud에 mongoDB를 띄워서 데이터를 넣었으나 시간이 지나면 계속 데이터가 사라지는 문제점을 확인.

#### 4-1. 팀원들과 분산작업 (에러 해결)
    - 조사 끝에 누군가가 해킹을 해서 침입을 한 것으로 파악
    - 원인 : 방화벽 설정을 안함
    - 방화벽 설정을 통하여 특정 ip만 접속 할 수 있게 ip설정을 하여 침입을 방지
<br>

### 5. Kafka에서 connenctor 실패
    - kafka와 logstash와 연동은 됐지만 싱크 커넥터를 통해 BigQuery에 데이터가 안들어감.
<br>

#### 5-1. python 코드로 대체 (문제 해결)
    - python에서 임의로 꺼내줄 수 있는 코드를 짜서 BigQuery에 보내줌.
<br>

## 담당역할
<br>

### 1. 영화, TV show 대량 데이터 수집 및 전처리
<br>

    - TMDB API를 활용하여 파이썬 코드를 기간별로 구분지어 영화 정보를 약 60만건 수집하게 되었습니다.
    - 하지만 오래된 공연DVD와 같은 영화, TV 프로그램이외의 data가 절반 이상을 차지하였으며,
    - 데이터를 구분지을 key가 별도로 없었기에 전처리에 어려움이 있으며, 프로젝트 데이터로서의 가치가 부족하다고 판단하였습니다.

<br>

    - 셀레니움을 이용하여 netflix 사이트를 직접 크롤링하는 작업, "키노라이츠"라는 사이트에서도 데이터들을 모았습니다.

    - 각각의 사이트에서 세부정보를 가져오는 과정에서 과도한 트래픽으로 IP Blocking을 당하여 전체 데이터를 가져오는데 문제가 있었습니다.
 
    - 영화 고유 id값들을 6분할을 해서 팀원들이 각자의 ip에서 크롤링을 하였습니다.
 	  - json파일로 저장하여 병합하고 전처리를 하였습니다.
  
  **알게된 점**
 	
    - 데이터를 수집(크롤링)하는 과정에서 가져올 수 있는 정보들은 다 가져온 후 data lake에 적재 ->
          이후 전처리하여 datawharehouse를 구축한다.
    
   	- 프로젝트를 하며 전처리를 할때 각 파트별로 필요한 부분을 확실히 설정해놓으면 시간을 절약할 수 있다.
    
    - jira와 confluence 를 이용하여 일정 및 상황을 공유하면 팀원에게 따로 요청을 하지 않더라도 서로 필요한 부분을 공유 할 수 있다.



### 2. mongoDB에 데이터 적재, mongoDB와 django연동
  <br>
	  
  	- 영화 데이터 중 줄거리등의 컬럼에서 비정형 데이터가 생기는 경우가 있었습니다.
    - 이를 json 형식으로 저장하여 일어날 수 있는 이슈를 최소화 하고자 mongoDB를 사용했습니다.

    - 서비스용 DB를 구축하기 이전 K-ICT에서 무료로 할당받은 개발 서버를 이용하여 mongoDB를 구축하고 테스트용 DB로 이용할 수 있었습니다.
    - pymongo를 통해 django와 연동을 하는 과정에서 발생하는 이슈를 미리 모니터링 할 수 있었습니다.

    - 모니터링 과정에서는 OTT별로 collection을 나눠주고 분류했으며,
    - 실제 서비스용 DB를 구축함에 있어서는 OTT key를 따로 만들어 병합하는 과정을 거쳤으며,
    - 이를 통해 중복 영화 정보를 제거, 약 10만건 -> 4만건 으로 DB를 슬림하게 만들었습니다.

### 3. django
#### 3.1 django 개봉예정작 페이지 제작
    
  	- 영화 및 TV 프로그램의 개봉예정작 페이지를 제작하였습니다.
   	- mongoDB에 있는 데이터들을 django에 가져와서 view단에서 today를 기준으로 공개예정일을 계산하여 페이지로 구현하였습니다.
    - 각각의 영화 데이터가 어디에서 볼 수 있는지도 포스터 우측상단에서 보여줄 수 있게 작업하였습니다.

#### 3.2 pagenation 코드 수정

    - db 구축 및 page 작업을 같이하던 팀원의 필터링 기능에서 필터를 해제하고 검색할 경우 data가 뜨지 않는 문제가 발생
    -> 해당 views에 조건문을 추가하여 설정해놓은 id값에 아무것도 추가되지 않았을경우 첫 페이지로 return되게 설정
  
**알게된 점**

    - 처음에는 mongoDB의 데이터를 django와 mongodb가 연동이 가능한 djongo를 이용하라는 글이 많아서 해당 방법을 시도하였지만,
    - mongodb에 추가적인 데이터를 삽입하는 작업이 아닌 data를 가져와서 보여주는 작업만 필요하였기에 pymongo로도 충분히 구현 가능하다는 것을 알 수 있었습니다.

### 4. Airflow를 통한 자동화 
<br>   	
  #### 4.1 크롤링 덱 자동화
  
    - 팀원들과 함께 각자 작성해놓은 크롤링 코드를 전체적으로 통일하는 작업을 하였습니다.
  
    - 각 페이지에서 가져올 수 있는 데이터가 달랐기에 관람등급과 같은 데이터를 통일하는 전처리 작업을 해야했습니다.

  **Work Flow**
  
    - Airflow를 통해 MEGABOX, CGV, DAUM영화 에서 순차적으로 데이터를 수집 -> 
    
    - 중복 값은 제거하며, OTT 컬럼에 해당되는 페이지를 추가 ->
    
    - mongodb에 데이터를 적재 ->
    
    - mongodb에서 자동으로 생성된 고유한 정보인 _id필드를 기준으로 poster image들의 이름을 설정->
    
    - Google Cloud Storage에 적재하는 과정을 배치로 airflow 자동화를 하였습니다.

    
  #### 4.2 사용자기반 추천 모델 자동화
    - Airflow로 추천모델을 구축해놓은 컨테이너로 ssh 연결
    - 하루에 한번 추천 모델을 실행
    - 실행 결과 slack api를 이용하여 확인
  
  **Work Flow**
  
    - django에서 Bigquery에 적재한 사용자의 로그데이터를 분석 ->
    
    - 사용자의 예상평점을 분석 및 추천 미디어 100개를 산출 ->
    
    - Redis로 전송하여 사용자에게 추천


 <div align=center><h1>📚 STACKS</h1></div>

<div align=center> 
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <br>
  
  <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white">
  <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white">
  <br>
  
  <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white"> 
  <img src="https://img.shields.io/badge/mongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white">
  <br>
  
  <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white">
  <img src="https://img.shields.io/badge/logstash-005571?style=for-the-badge&logo=logstash&logoColor=white">
  <br>
  
  <img src="https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white">
  <img src="https://img.shields.io/badge/apachekafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white">
  <img src="https://img.shields.io/badge/apacheairflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white">
  <br>
    
  <img src="https://img.shields.io/badge/ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> 
  <img src="https://img.shields.io/badge/googlecloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white"> 
  <br>
  
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
  <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> 
  <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> 
  <br>

  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
  <img src="https://img.shields.io/badge/fontawesome-339AF0?style=for-the-badge&logo=fontawesome&logoColor=white">
  <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
  <br>
</div>
