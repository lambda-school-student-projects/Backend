import Cocoa

// This won't access URLSessionWebSocketTask bc this project was done in the previous version of Xcode.  So it has to be cut paste and put into the latest Xcode


class SocketController {
    
    @available(iOS 13.0, *)
    open func webSocketTask(with url: URL) -> URLSessionWebSocketTask
    
    
    open func cancel(with closeCode: URLSessionWebSocketTask.CloseCode, reason: Data?)
    
    func disconnect() {
        webSocketTask.cancel(with: .goingAway, reason: nil)
    }
    
    let urlSession = URLSession(configuration: .default)
    let webSocketTask = urlSession.webSocketTask(with: "ws://demos.kaazing.com/echo")
    
    webSocketTask.resume()
    
    let message = URLSessionWebSocketTask.Message.string("Hello World")
    
    webSocketTask.send(message) { error in
        if let error = error {
            print("WebSocket sending error: \(error)")
        }
    }
    
    
    func readMessage()  {
        webSocketTask.receive { result in
            switch result {
            case .failure(let error):
                print("Failed to receive message: \(error)")
            case .success(let message):
                switch message {
                case .string(let text):
                    print("Received text message: \(text)")
                case .data(let data):
                    print("Received binary message: \(data)")
                @unknown default:
                    fatalError()
                }
                
                self.readMessage()
            }
        }
    }
    
    
}




@available(iOS 13.0, *)
public protocol URLSessionWebSocketDelegate : URLSessionTaskDelegate {
    
    optional func urlSession(_ session: URLSession, webSocketTask: URLSessionWebSocketTask, didOpenWithProtocol protocol: String?)
    
    optional func urlSession(_ session: URLSession, webSocketTask: URLSessionWebSocketTask, didCloseWith closeCode: URLSessionWebSocketTask.CloseCode, reason: Data?)
}

