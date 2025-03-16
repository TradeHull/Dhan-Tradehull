#### Double check if below steps are done on your end before running the program
1.	Check if you subscribed to Dhan Trading Api and Data Api
2.	see if you have updated the token and client_id in below files
Dhan_codebase usage > token_id
Dhan_websocket > access_token
in the both files you need to replace by your Api token
3.	Check if in Websocket.xlsx
<br> In Column A, check if script name and spelling is correct, and no FNO script should be expired.
<br> In Column B, see if exchange is proper
- for NSE equity use - NSE
- for BSE equity use - BSE
- for NFO use - NFO
- for BFO use - BFO
- for NSE INDICES - NSE_IDX
- for BSE INDICES - BSE_IDX
- for MCX - MCX
4.	Double check if you are running Dhan_websocket.py in CMD
5.	See if you have enabled editing in excel, (we need to give it permission to edit)

![image_alt](https://github.com/TradeHull/Dhan-Tradehull/blob/main/Algo%20Trading%20Series%201/Session%203/Picture1.png?raw=true)
