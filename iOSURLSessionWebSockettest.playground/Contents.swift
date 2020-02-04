import Cocoa

// This won't access URLSessionWebSocketTask bc this project was done in the previous version of Xcode.  So it has to be cut paste and put into the latest Xcode


class SocketController {
    
    @available(iOS 13.0, *)
    open func webSocketTask(with url: URL) -> URLSessionWebSocketTask
    
    
    let urlSession = URLSession(configuration: .default)
    let webSocketTask = urlSession.webSocketTask(with: "enterURLHere")
    
    webSocketTask.resume()
    
    let message = URLSessionWebSocketTask.Message.string("Hello World")
    
    webSocketTask.send(message) { error in
        if let error = error {
            print("WebSocket sending error: \(error)")
        }
    }
}

