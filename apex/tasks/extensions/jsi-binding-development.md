# Task: jsi-binding-development

```yaml
id: jsi-binding-development
version: "1.0.0"
title: "JSI Binding Development"
description: >
  Designs and implements JavaScript Interface (JSI) bindings for
  synchronous native access in React Native. Covers C++ JSI host
  objects, TurboModule integration, type-safe bindings, memory
  management, and error handling. Produces production-ready JSI
  bindings that eliminate bridge overhead for performance-critical
  native operations.
elicit: false
owner: mobile-eng
executor: mobile-eng
outputs:
  - JSI binding architecture design
  - C++ HostObject implementation
  - Platform-specific native implementations (iOS/Android)
  - TypeScript type definitions
  - Memory management strategy
  - JSI binding specification document
```

---

## When This Task Runs

This task runs when:
- A native operation needs synchronous access from JS (no bridge latency)
- Existing bridge-based native modules are a performance bottleneck
- Implementing real-time features (audio processing, sensor data, cryptography)
- Migrating native modules to New Architecture (TurboModules via JSI)
- Building custom native functionality not covered by Expo modules
- `*jsi-binding` or `*jsi-dev` is invoked

This task does NOT run when:
- The native module can work asynchronously (use standard TurboModule)
- Expo modules cover the functionality (use Expo API)
- The task is about JS-only performance (use `rn-performance-optimization`)
- The project uses Expo managed workflow without custom native code

---

## Execution Steps

### Step 1: Evaluate JSI Necessity

Determine if JSI is the right approach (vs TurboModule, Expo Module, or bridge).

**Decision matrix:**
| Requirement | Standard Module | TurboModule | JSI HostObject |
|-------------|----------------|-------------|----------------|
| Async native call | Yes | Yes | Yes |
| Sync native call | No | Partial (sync methods) | Yes |
| Bridge overhead acceptable | Yes | Lower | Zero |
| Codegen type safety | No | Yes (Codegen) | Manual |
| Complexity | Low | Medium | High |
| Real-time (<1ms latency) | No | No | Yes |

**Use JSI when:**
- Synchronous access is critical (sensor polling, frame-by-frame processing)
- Bridge serialization is the bottleneck (large data, high frequency)
- Building a shared C++ library (runs on both iOS and Android from one codebase)
- Need to share memory between JS and native (e.g., ArrayBuffer for audio)

**Don't use JSI when:**
- Async is acceptable (most API calls, file I/O, notifications)
- TurboModule covers the use case (most native modules)
- Expo module exists for the functionality

**Output:** JSI necessity evaluation with rationale.

### Step 2: Design JSI HostObject

Design the C++ HostObject that exposes native functionality to JS.

**HostObject structure:**
```cpp
#include <jsi/jsi.h>

using namespace facebook::jsi;

class CryptoHostObject : public HostObject {
public:
  CryptoHostObject() = default;

  Value get(Runtime& runtime, const PropNameID& name) override {
    auto methodName = name.utf8(runtime);

    if (methodName == "sha256") {
      return Function::createFromHostFunction(
        runtime, name, 1, // 1 argument
        [](Runtime& runtime, const Value& thisVal,
           const Value* args, size_t count) -> Value {
          if (count < 1 || !args[0].isString()) {
            throw JSError(runtime, "sha256 expects a string argument");
          }
          auto input = args[0].asString(runtime).utf8(runtime);
          auto hash = computeSHA256(input); // Native implementation
          return String::createFromUtf8(runtime, hash);
        }
      );
    }

    if (methodName == "randomBytes") {
      return Function::createFromHostFunction(
        runtime, name, 1,
        [](Runtime& runtime, const Value& thisVal,
           const Value* args, size_t count) -> Value {
          auto size = static_cast<int>(args[0].asNumber());
          auto bytes = generateRandomBytes(size);
          // Return as ArrayBuffer for zero-copy
          auto buffer = ArrayBuffer(runtime, size);
          memcpy(buffer.data(runtime), bytes.data(), size);
          return std::move(buffer);
        }
      );
    }

    return Value::undefined();
  }

  std::vector<PropNameID> getPropertyNames(Runtime& runtime) override {
    return PropNameID::names(runtime, "sha256", "randomBytes");
  }
};
```

**Design rules:**
- One HostObject per domain (e.g., CryptoHostObject, SensorHostObject)
- Methods should be pure functions when possible (no hidden state)
- Use `ArrayBuffer` for binary data (zero-copy transfer)
- Throw `JSError` for invalid arguments (not native exceptions)
- Keep HostObject methods small and focused

**Output:** HostObject design with method specifications.

### Step 3: Implement Platform Bindings

Connect the C++ HostObject to iOS (Objective-C++) and Android (JNI).

**iOS integration (Objective-C++):**
```objc
// CryptoModule.mm
#import <React/RCTBridge+Private.h>
#import <jsi/jsi.h>
#import "CryptoHostObject.h"

@interface CryptoModule : NSObject <RCTBridgeModule>
@end

@implementation CryptoModule

RCT_EXPORT_MODULE()

+ (BOOL)requiresMainQueueSetup { return YES; }

- (void)setBridge:(RCTBridge *)bridge {
  auto runtime = reinterpret_cast<facebook::jsi::Runtime*>(
    bridge.runtime
  );
  auto hostObject = std::make_shared<CryptoHostObject>();
  runtime->global().setProperty(
    *runtime,
    "CryptoNative",
    Object::createFromHostObject(*runtime, hostObject)
  );
}

@end
```

**Android integration (JNI + C++):**
```cpp
// CryptoModule.cpp (JNI bridge)
#include <fbjni/fbjni.h>
#include <ReactCommon/CallInvokerHolder.h>
#include "CryptoHostObject.h"

extern "C" JNIEXPORT void JNICALL
Java_com_myapp_CryptoModule_install(
    JNIEnv* env, jobject thiz, jlong runtimePtr) {
  auto runtime = reinterpret_cast<facebook::jsi::Runtime*>(runtimePtr);
  auto hostObject = std::make_shared<CryptoHostObject>();
  runtime->global().setProperty(
    *runtime,
    "CryptoNative",
    jsi::Object::createFromHostObject(*runtime, hostObject)
  );
}
```

**Build configuration:**
- iOS: Add C++ files to Xcode project, set C++ standard to C++17
- Android: Configure CMakeLists.txt with JSI and fbjni dependencies
- Both: Share the C++ HostObject code between platforms

**Output:** Platform-specific binding implementations for iOS and Android.

### Step 4: Create TypeScript Definitions

Provide type-safe TypeScript access to the JSI bindings.

```typescript
// src/native/CryptoNative.ts

declare global {
  var CryptoNative: {
    sha256(input: string): string;
    randomBytes(size: number): ArrayBuffer;
  };
}

// Type-safe wrapper with runtime check
export function getCryptoNative() {
  if (!global.CryptoNative) {
    throw new Error(
      'CryptoNative is not installed. ' +
      'Make sure the native module is linked and the app is rebuilt.'
    );
  }
  return global.CryptoNative;
}

// Usage
export function sha256(input: string): string {
  return getCryptoNative().sha256(input);
}

export function randomBytes(size: number): ArrayBuffer {
  return getCryptoNative().randomBytes(size);
}
```

**Type definition rules:**
- Declare global type for the HostObject
- Create wrapper functions that check availability
- Provide helpful error messages if native module is missing
- Export individual functions (not the raw global)
- Document parameter constraints (e.g., max buffer size)

**Output:** TypeScript type definitions with runtime availability checks.

### Step 5: Plan Memory Management

Design memory management strategy to prevent leaks and crashes.

**Memory management rules:**
| Concern | Strategy |
|---------|----------|
| HostObject lifetime | Shared pointer (`std::shared_ptr`) ensures cleanup |
| ArrayBuffer ownership | JS runtime manages buffer lifecycle |
| String copies | Use `StringBuffer` for large strings to avoid copies |
| Callback captures | Weak references to avoid preventing GC |
| Thread safety | Use mutexes for shared mutable state |
| Native resource cleanup | Destructor in HostObject releases native resources |

**Common memory pitfalls:**
- Capturing `Runtime&` in lambda closures (Runtime may be destroyed)
- Allocating large native buffers without tracking
- Circular references between HostObjects
- Not releasing native resources (file handles, network connections)

**Destructor pattern:**
```cpp
class SensorHostObject : public HostObject {
  ~SensorHostObject() override {
    // Release native resources
    stopSensorListening();
    closeNativeHandle();
  }
};
```

**Output:** Memory management strategy with common pitfall prevention.

### Step 6: Document JSI Binding Specification

Compile complete specification for the JSI module.

**Documentation includes:**
- Necessity evaluation (from Step 1)
- HostObject API reference (from Step 2)
- Platform integration guide (from Step 3)
- TypeScript API reference (from Step 4)
- Memory management guidelines (from Step 5)
- Testing strategy (unit + integration)
- Troubleshooting guide (common errors and fixes)

**Output:** Complete JSI binding specification document.

---

## Quality Criteria

- JSI calls must be synchronous with <1ms overhead
- Memory must not leak after component unmount and module cleanup
- TypeScript types must match native implementation exactly
- Both iOS and Android must pass identical test suite
- Error handling must produce helpful messages (not native crashes)

---

*Squad Apex — JSI Binding Development Task v1.0.0*

---

## Quality Gate

```yaml
gate:
  id: QG-jsi-binding-development
  blocker: true
  criteria:
    - "All outputs listed in YAML header must be produced"
    - "JSI calls must complete in <1ms (synchronous)"
    - "No memory leaks after component lifecycle test"
    - "TypeScript types match native implementation"
    - "Both iOS and Android pass identical test suite"
    - "Invalid arguments throw JSError, not native crash"
  on_fail: "BLOCK — return to executor with specific gaps listed"
  on_pass: "Mark task complete, deliver outputs to handoff target"
```

---

## Handoff

| Field | Value |
|-------|-------|
| Delivers to | `@cross-plat-eng` or `@apex-lead` |
| Artifact | JSI binding specification with HostObject implementation, platform bindings, TypeScript types, and memory management plan |
| Next action | Integrate into app via `@mobile-eng` or test cross-platform via `@qa-xplatform` |
