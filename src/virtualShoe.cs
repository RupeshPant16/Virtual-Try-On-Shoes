using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class virtualShoe : MonoBehaviour
{
    string recvStr;
    int flag;
    public RawImage my_img;
    Socket serverSocket;
    IPAddress ip;
    IPEndPoint ipEnd;
    string[] arr = new string[1024];
    string[] cent_arr = new string[1024];
    byte[] recvData = new byte[1024]; //The received data must be bytes
    byte[] sendData = new byte[1024]; //The data sent must be bytes
    byte[] centr = new byte[1024];
    string cent;
    byte[] recv_img;
    int recvLen; //Received data length
    byte[] recv_keypoint = new byte[1024];
    string recv_keypoint_str;
    public float shoe_scale = 2f;
    public GameObject Cube;
    float R_center_x = 0f;
    float R_center_y = 0f;


    int itr = 1;

    Thread connectThread;


    void InitSocket()
    {
        //Define the IP and port of the server, and the port corresponds to the server
        ip = IPAddress.Parse("127.0.0.1"); //It can be a local area network or Internet ip, here is the machine
        ipEnd = new IPEndPoint(ip, 9000);


        //Open a thread connection, necessary, otherwise the main thread is stuck
        connectThread = new Thread(new ThreadStart(SocketReceive));
        connectThread.Start();
    }

    void SocketConnet()
    {
        if (serverSocket != null)
            serverSocket.Close();
        //Define the socket type, which must be defined in the child thread
        serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        print("ready to connect");
        //connection
        serverSocket.Connect(ipEnd);

        //Output the string received for the first connection
        //recvLen = serverSocket.Receive(recvData);
        //recvStr = Encoding.ASCII.GetString(recvData, 0, recvLen);
        //print(recvStr);
    }


    void SocketSend(string sendStr)
    {
        //Clear the sending buffer
        sendData = new byte[1024];
        //Data type conversion
        sendData = Encoding.ASCII.GetBytes(sendStr);
        //send
        serverSocket.Send(sendData, sendData.Length, SocketFlags.None);
    }



    void SocketReceive()
    {
        SocketConnet();
        //Continuously receive data from the server
        while (true)
        {
            SocketSend("OK_1");

            recvData = new byte[1024];
            recvLen = serverSocket.Receive(recvData);
            if (recvLen == 0)
            {
                print("reconnecting...");
                SocketConnet();
                continue;
            }

            SocketSend("OK_2");

            recvStr = Encoding.ASCII.GetString(recvData, 0, recvLen);
            int img_size = Convert.ToInt32(recvStr);
            //int cou = 0;
            flag = 0;
            recv_img = new byte[img_size];
            int recv_img_len = serverSocket.Receive(recv_img);
            if (img_size != recv_img_len)
            {
                print("error");
            }
            else
            {
                flag = 1;

                SocketSend("OK_3");

                recv_keypoint = new byte[1024];
                int recv_keypoint_len = serverSocket.Receive(recv_keypoint);
                recv_keypoint_str = Encoding.ASCII.GetString(recv_keypoint, 0, recv_keypoint_len);
                //print(recv_keypoint_str);
                arr = recv_keypoint_str.Split(',');
                //print(arr[0] + " " + arr[1] + " " + arr[2] + " " + arr[3] + "\n");
                centr = new byte[1024];
                int recv_cent = serverSocket.Receive(centr);
                cent = Encoding.ASCII.GetString(centr, 0, recv_cent);
                cent_arr = cent.Split(',');

            }
        }
    }

    void SocketQuit()
    {
        if (connectThread != null)
        {
            connectThread.Interrupt();
            connectThread.Abort();
        }
        if (serverSocket != null)
            serverSocket.Close();
        print("diconnect");
    }

    // Start is called before the first frame update
    void Start()
    {
        my_img.texture = new Texture2D(640, 480, TextureFormat.RGB24, false);
        InitSocket();

    }

    // Update is called once per frame
    void Update()
    {
        //if (flag == 1)
        //{
        //Application.targetFrameRate = 30;
        var texture = my_img.texture as Texture2D;

        //print("Image recieved");
        texture.LoadImage(recv_img);
        print("load image" + itr++);
        texture.Apply();
        float f_len = Int32.Parse(arr[2]) - Int32.Parse(arr[3]);
        float f_wid = Int32.Parse(arr[0]) - Int32.Parse(arr[1]);
        R_center_y = (Int32.Parse(arr[2]) + Int32.Parse(arr[3])) / 2f;
        R_center_x = (Int32.Parse(arr[0]) + Int32.Parse(arr[1])) / 2f;
        float x = float.Parse(cent_arr[0]);
        float y = float.Parse(cent_arr[1]);
        //Cube.transform.eulerAngles = new Vector3(-20f, 0f, 0f);
        //Cube.transform.Rotate(new Vector3(0, 145, 45), Space.Self);
        Cube.GetComponent<Transform>().localPosition = new Vector3(x - 300f, -(y - 250f), -3);
        print(f_wid + " " + f_len);
        Cube.transform.localScale = new Vector3(f_wid/90, f_len/150 ,f_wid/200 ); //arun
        //Cube.transform.localScale = new Vector3(f_wid *10 /12, f_len*10 / 17, f_wid*10 / 17); //aryan

        //print("Image Applied");


        //}

    }

    void OnApplicationQuit()
    {
        SocketQuit();
    }
}