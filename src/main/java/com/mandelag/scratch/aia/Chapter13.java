package com.mandelag.scratch.aia;


import akka.actor.ActorSystem;
import akka.stream.ActorMaterializer;
import akka.stream.IOResult;
import akka.stream.javadsl.FileIO;
import akka.stream.javadsl.RunnableGraph;
import akka.stream.javadsl.Sink;
import akka.stream.javadsl.Source;
import akka.util.ByteString;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.concurrent.CompletionStage;

public class Chapter13 {
  public static void main(String[] args) throws IOException {
    ActorSystem system = ActorSystem.create("learning-akka-streams");

    Source<ByteString, CompletionStage<IOResult>> logSource = FileIO.fromPath(Paths.get("src", "main", "resources", "TPS_Jakarta_2017.json"));
    Sink<ByteString, CompletionStage<IOResult>> copyDestination = FileIO.toPath(Paths.get("src", "main", "resources", "ouput.json"));

    RunnableGraph<CompletionStage<IOResult>> graph = logSource.to(copyDestination);

    CompletionStage<IOResult> future = graph.run(ActorMaterializer.create(system));

    future.thenAccept(System.out::println);

    System.in.read();
    system.terminate();
  }
}
