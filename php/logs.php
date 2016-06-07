<?php

/**
 * Created by PhpStorm.
 * User: LiChenJun
 * Date: 16/6/2
 * Time: 下午3:16
 */

$log  = new LogsUpload();
if($_POST){
    echo 33;
    $log->upload();
}elseif($_GET['test'] == 1){
    $log->test();
}
class LogsUpload
{
//    public $filepath = '/MM/HTML/Source/avatar/';
    public $filepath = '/data/logfile/';

    public $redis_conf = [
        'host'=>'127.0.0.1',
        'port'=> '6379',
        'queue_key'=>'logfile'
    ];
    public function upload(){
        if ($_FILES["file"]["type"] == "application/zip")
        {
            if ($_FILES["file"]["error"] > 0)
            {
                $this->returnJson(100,'文件上传失败');
            }
            else
            {
                echo $path = $this->filepath .time(). $_FILES["file"]["name"];
                move_uploaded_file($_FILES["file"]["tmp_name"], $path);
                //写进redis中
                $redis = new Redis();
                $redis->connect($this->redis_conf['host'],$this->redis_conf['redis.port']);
                $ret = $redis->lPush($this->redis_conf['queue_key'],$path);
                if($ret >0){
                    $this->returnJson(200,'成功');
                }else{
                    $this->returnJson(100,'失败');
                }
            }
        }
        else
        {
            $this->returnJson(100, '格式错误');
        }
    }

    public function test(){
        $str = <<<EOT
            <html>
<body>

<form action="" method="post"
enctype="multipart/form-data">
<label for="file">Filename:</label>
<input type="file" name="file" id="file" />
<br />
<input type="submit" name="submit" value="Submit" />
</form>

</body>
</html>
EOT;
        echo $str;
    }

    /**
     * 返回输出JSON
     * @param int $code 错误代码
     * @param string $data 返回数据
     * @param string $msg  错误信息
     */
    public function returnJson( $code = 200, $msg = ''){
        $ret = array('code'=>$code, 'msg'=>$msg);
        echo json_encode($ret);
        exit();
    }
}
