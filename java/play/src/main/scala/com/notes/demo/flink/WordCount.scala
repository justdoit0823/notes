package com.notes.demo.flink

import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time

case class WordWithCount(word: String, count: Long)

object WordCount {

  def main(args: Array[String]): Unit = {

    val host = "127.0.0.1"
    val port = 11111

    val env = StreamExecutionEnvironment.getExecutionEnvironment
    val text = env.socketTextStream(host, port, '\n')

    val windowCounts = text.flatMap { w => w.split("\\s") }
      .map { w => WordWithCount(w, 1) }
      .keyBy("word")
      .timeWindow(Time.seconds(5))
      .sum("count")

    windowCounts.print()

    env.execute("Socket Window WordCount")
  }
}
