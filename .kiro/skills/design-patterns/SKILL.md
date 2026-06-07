---
name: design-patterns
description: Software design patterns for architecture and implementation decisions. Use when designing systems (Planner), generating code (Generator), or evaluating structural quality (Evaluator). Covers Creational, Structural, and Behavioral patterns with when-to-use guidance.
keywords: design patterns, factory, singleton, strategy, observer, adapter, repository, dependency injection, decorator, facade, builder, CQRS, mediator, architecture
---

# Design Patterns Reference

> Use this skill when making architecture decisions, implementing common solutions, or evaluating code structure.

---

## Part A: Pattern Selection Guide (Planner)

### When to Use Which Pattern

| Problem | Pattern | Why |
|---------|---------|-----|
| Need to create objects without specifying exact class | Factory Method / Abstract Factory | Decouples creation from usage |
| Complex object with many optional params | Builder | Readable construction, immutable objects |
| Need exactly one instance | Singleton | Global access point (use sparingly) |
| Need to switch algorithms at runtime | Strategy | OCP-compliant behavior swapping |
| Multiple objects need to react to state changes | Observer | Loose coupling between publisher/subscribers |
| Incompatible interfaces need to work together | Adapter | Bridge between old and new code |
| Need to simplify a complex subsystem | Facade | Single entry point, hide complexity |
| Need to add behavior without modifying class | Decorator | Composable enhancements |
| Need to separate read/write operations | CQRS | Scalability, different models for read vs write |
| Need to decouple request sender from handler | Mediator / Command | Reduce direct dependencies |
| Need to abstract data access | Repository | Testable, swappable data layer |
| Need to define a skeleton algorithm | Template Method | Reuse structure, vary steps |
| Need to traverse a collection | Iterator | Uniform access without exposing internals |
| Need to save/restore object state | Memento | Undo functionality |

### Architecture-Level Patterns

| Pattern | When | Key Benefit |
|---------|------|-------------|
| Layered Architecture | Most CRUD apps | Separation of concerns |
| Repository + Unit of Work | Data access | Testability, transaction management |
| CQRS | Read-heavy or complex domains | Optimized read/write models |
| Event-Driven | Async workflows, microservices | Loose coupling, scalability |
| Mediator (MediatR) | Complex request handling | Decoupled handlers, cross-cutting concerns |
| Specification | Complex business rules / filtering | Composable, testable rules |

---

## Part B: Implementation Guide (Generator)

### Creational Patterns

#### Factory Method
```typescript
// When: Creating objects where the exact type varies
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) { console.log(message); }
}

class FileLogger implements Logger {
  log(message: string) { /* write to file */ }
}

class LoggerFactory {
  static create(type: 'console' | 'file'): Logger {
    switch (type) {
      case 'console': return new ConsoleLogger();
      case 'file': return new FileLogger();
      default: throw new Error(`Unknown logger type: ${type}`);
    }
  }
}
```

#### Builder
```typescript
// When: Complex object construction with many optional parameters
class QueryBuilder {
  private table = '';
  private conditions: string[] = [];
  private orderBy = '';
  private limit?: number;

  from(table: string): this { this.table = table; return this; }
  where(condition: string): this { this.conditions.push(condition); return this; }
  order(field: string): this { this.orderBy = field; return this; }
  take(n: number): this { this.limit = n; return this; }

  build(): string {
    let sql = `SELECT * FROM ${this.table}`;
    if (this.conditions.length) sql += ` WHERE ${this.conditions.join(' AND ')}`;
    if (this.orderBy) sql += ` ORDER BY ${this.orderBy}`;
    if (this.limit) sql += ` LIMIT ${this.limit}`;
    return sql;
  }
}
```

### Structural Patterns

#### Repository
```typescript
// When: Abstracting data access for testability
interface IUserRepository {
  getById(id: number): Promise<User | null>;
  getAll(): Promise<User[]>;
  create(user: CreateUserDto): Promise<User>;
  update(id: number, data: UpdateUserDto): Promise<User>;
  delete(id: number): Promise<void>;
}

// Concrete implementation
class SqlUserRepository implements IUserRepository {
  constructor(private db: Database) {}

  async getById(id: number): Promise<User | null> {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
  // ... other methods
}

// In tests: use MockUserRepository implementing same interface
```

#### Adapter
```typescript
// When: Making incompatible interfaces work together
interface PaymentGateway {
  charge(amount: number, currency: string): Promise<PaymentResult>;
}

// Third-party SDK with different interface
class StripeSDK {
  createCharge(params: { amount_cents: number; currency: string }) { /* ... */ }
}

// Adapter bridges the gap
class StripeAdapter implements PaymentGateway {
  constructor(private stripe: StripeSDK) {}

  async charge(amount: number, currency: string): Promise<PaymentResult> {
    const result = await this.stripe.createCharge({
      amount_cents: amount * 100,
      currency,
    });
    return { success: true, transactionId: result.id };
  }
}
```

#### Decorator
```typescript
// When: Adding behavior without modifying original class
interface INotificationService {
  send(message: string, recipient: string): Promise<void>;
}

class EmailNotification implements INotificationService {
  async send(message: string, recipient: string) { /* send email */ }
}

// Decorator adds logging without modifying EmailNotification
class LoggingNotification implements INotificationService {
  constructor(
    private inner: INotificationService,
    private logger: ILogger,
  ) {}

  async send(message: string, recipient: string) {
    this.logger.info(`Sending notification to ${recipient}`);
    await this.inner.send(message, recipient);
    this.logger.info(`Notification sent successfully`);
  }
}
```

### Behavioral Patterns

#### Strategy
```typescript
// When: Algorithm needs to vary at runtime
interface PricingStrategy {
  calculate(basePrice: number): number;
}

class RegularPricing implements PricingStrategy {
  calculate(basePrice: number) { return basePrice; }
}

class MemberPricing implements PricingStrategy {
  calculate(basePrice: number) { return basePrice * 0.9; }
}

class VIPPricing implements PricingStrategy {
  calculate(basePrice: number) { return basePrice * 0.75; }
}

class OrderService {
  constructor(private pricing: PricingStrategy) {}

  calculateTotal(items: Item[]): number {
    const base = items.reduce((sum, i) => sum + i.price, 0);
    return this.pricing.calculate(base);
  }
}
```

#### Observer / Event
```typescript
// When: Multiple components need to react to state changes
type EventHandler<T> = (data: T) => void;

class EventBus {
  private handlers = new Map<string, EventHandler<any>[]>();

  on<T>(event: string, handler: EventHandler<T>): void {
    const list = this.handlers.get(event) || [];
    list.push(handler);
    this.handlers.set(event, list);
  }

  emit<T>(event: string, data: T): void {
    const list = this.handlers.get(event) || [];
    list.forEach(handler => handler(data));
  }
}

// Usage: loosely coupled modules
eventBus.on('user.created', (user) => sendWelcomeEmail(user));
eventBus.on('user.created', (user) => initializeProfile(user));
eventBus.on('user.created', (user) => logAnalytics('signup', user));
```

#### Template Method
```typescript
// When: Define algorithm skeleton, let subclasses fill in steps
abstract class DataExporter {
  // Template method — defines the skeleton
  async export(): Promise<void> {
    const data = await this.fetchData();
    const transformed = this.transform(data);
    await this.write(transformed);
    await this.notify();
  }

  protected abstract fetchData(): Promise<any[]>;
  protected abstract transform(data: any[]): string;
  protected abstract write(content: string): Promise<void>;

  // Default implementation (can be overridden)
  protected async notify(): Promise<void> { /* no-op */ }
}

class CsvExporter extends DataExporter {
  protected async fetchData() { return db.query('SELECT * FROM orders'); }
  protected transform(data: any[]) { return toCsv(data); }
  protected async write(content: string) { await fs.writeFile('export.csv', content); }
}
```

---

## Part C: Evaluation Criteria (Evaluator)

### Pattern Usage Checklist

| Check | Pass | Fail |
|-------|------|------|
| Pattern fits the problem | Solves actual complexity | Over-engineering simple logic |
| Interface defined | External deps behind interface | Direct coupling to concrete class |
| SRP maintained | Each class has one job | God class with pattern inside |
| Testable | Can unit test with mock | Pattern creates untestable coupling |
| Not over-applied | Used where complexity warrants | Factory for single implementation |

### Common Anti-Patterns to Flag

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|----------------|
| Singleton abuse | Hidden global state, untestable | DI with scoped lifetime |
| Factory for 1 type | Unnecessary indirection | Direct instantiation |
| Observer spaghetti | Unpredictable event chains | Explicit mediator or direct calls |
| Decorator hell | 5+ layers wrapping | Consolidate or use AOP |
| Premature abstraction | Interface with 1 implementation | YAGNI — add when second impl needed |
| Repository over ORM | Repository that just proxies ORM | Use ORM directly for simple CRUD |

### Scoring Modifiers

| Condition | Modifier |
|-----------|----------|
| Appropriate pattern selection for the problem | +5 |
| Pattern enables easy testing | +3 |
| Over-engineered (pattern where none needed) | -5 |
| Missing pattern where clearly needed (e.g., raw SQL everywhere, no repository) | -5 |
| God class / no separation of concerns | -10 |

### When Patterns are NOT Needed

- Simple CRUD with < 3 entities → direct implementation is fine
- Single implementation of an interface → skip the interface until you need a second
- Prototype / proof of concept → clarity over structure
- The pattern adds more code than it removes complexity

---

## Quick Decision Matrix

```
Is the logic complex / likely to change?
├── No → Write it directly (YAGNI)
└── Yes
    ├── Is it about CREATING objects?
    │   ├── Many params → Builder
    │   ├── Multiple types → Factory
    │   └── One instance → Singleton (careful!)
    ├── Is it about STRUCTURING relationships?
    │   ├── Incompatible interface → Adapter
    │   ├── Add behavior → Decorator
    │   ├── Simplify subsystem → Facade
    │   └── Abstract data access → Repository
    └── Is it about BEHAVIOR?
        ├── Swap algorithm → Strategy
        ├── React to changes → Observer
        ├── Decouple sender/handler → Command/Mediator
        └── Algorithm skeleton → Template Method
```

---

*This skill should be activated when designing architecture, implementing common solutions, or evaluating structural quality.*
