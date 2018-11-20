package com.mandelag.scratch.jia;

import akka.http.javadsl.model.HttpRequest;
import akka.http.javadsl.model.HttpResponse;
import akka.stream.ActorMaterializer;
import akka.stream.javadsl.Sink;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletionStage;

import akka.actor.ActorSystem;
import akka.http.javadsl.*;


public class Chapter3 {

  private static ActorSystem system;

  public static void main(String[] args) throws IOException {
    system = ActorSystem.create("requester");
    loadData();
    System.in.read();
    system.terminate();
  }

  private static void loadData() throws IOException {
    Http http = Http.get(system);

    System.out.println(Paths.get("").toAbsolutePath().toFile().isDirectory());
    Path toData = Paths.get("src", "main", "resources", "TPS_Jakarta_2017.json");
    // kalau pakai backslash ngga bisa di *nix. Kalau pakai slash ngga bisa di Windows..?
    System.out.println(toData.toFile().exists());
    ObjectMapper om = new ObjectMapper();
    List<Map<String, String>> data = om.readValue(toData.toFile(), List.class);
    Base64.Encoder encoder = Base64.getEncoder();
    data.parallelStream()
        .map(m -> m.get("kelurahan"))
        .map(kelurahan -> {
          byte[] encoded = encoder.encode(String.format("getTps~20181120Sm4RTC1tY~%s", kelurahan).getBytes());
          return new String(encoded);
        }).map(command -> String.format("http://crop.jakarta.go.id/ajax/apps_command.php?%s", command))
        .forEach(url -> {
          http.singleRequest(HttpRequest.create(url))
              .thenAccept(resp -> {
                resp.entity().getDataBytes().to(Sink.foreach((byteString) -> {
                  System.out.println(byteString.decodeString(StandardCharsets.UTF_8));
                })).run(ActorMaterializer.create(system));
              });
        });
  }

}
