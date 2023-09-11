{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.keys import Keys\n",
    "from selenium.webdriver.common.by import By\n",
    "from ping3 import ping, verbose_ping\n",
    "import time\n",
    "from selenium.webdriver.edge.service import Service as EdgeService\n",
    "from webdriver_manager.microsoft import EdgeChromiumDriverManager\n",
    "\n",
    "def klu_net_login():\n",
    "    try:\n",
    "        # driver = webdriver.Edge()\n",
    "        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))\n",
    "        driver.get(\"http://172.16.103.254:8090/httpclient.html\")\n",
    "        elem = driver.find_element(By.NAME, \"username\")\n",
    "        elem.clear()\n",
    "        elem.send_keys(\"klu1648\")\n",
    "        elem = driver.find_element(By.NAME, \"password\")\n",
    "        elem.clear()\n",
    "        elem.send_keys(\"L0g!n2n3t\")\n",
    "        elem.send_keys(Keys.RETURN)\n",
    "        time.sleep(5)\n",
    "        driver.switch_to.window(driver.window_handles[1])\n",
    "        driver.close()\n",
    "\n",
    "    except:\n",
    "        print(\"Cannot Login\")\n",
    "        time.sleep(10)\n",
    "\n",
    "\n",
    "while True:\n",
    "    p = ping('8.8.8.8')\n",
    "    if p > 0:\n",
    "        print(\"Network OK\")\n",
    "        time.sleep(10)\n",
    "    elif p == None:\n",
    "        p = klu_net_login()\n",
    "\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.2"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
